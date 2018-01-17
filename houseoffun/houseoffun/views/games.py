from django.db import IntegrityError
from django.db.models import Q
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages


from houseoffun.houseoffun.models import Game, GameSignup, Plugin


class GameForm(ModelForm):
    class Meta:
        model = Game
        exclude = ['game_master', 'status']

    plugins = ModelMultipleChoiceField(queryset=Plugin.objects.all(), widget=CheckboxSelectMultiple, required=False)


def game_list(request, template_name='games/list.html'):
    games = Game.objects.filter(
        Q(game_master=request.user) | Q(status__in=[Game.REGISTRATION, Game.PENDING, Game.RUNNING])
    ).defer('description')
    data = {'object_list': games}
    return render(request, template_name, data)


def game_create(request, template_name='games/form.html'):
    form = GameForm(request.POST or None)
    if form.is_valid():
        game = form.save(commit=False)
        game.game_master = request.user
        game.save()
        for plugin in request.POST.getlist('plugins'):
            game.plugins.add(plugin)
        return redirect('game_list')
    return render(request, template_name, {'form': form})


def game_view(request, pk, template_name='games/view.html'):
    game = get_object_or_404(Game, pk=pk)
    threads = False
    if game.has_plugin('Threads'):
        threads = game.thread_set.defer('text')
    user_signup = game.signups.filter(user=request.user).first()
    return render(request, template_name, {'game': game, 'threads': threads, 'user_signup': user_signup})


def game_update(request, pk, template_name='games/form.html'):
    game = get_object_or_404(Game, pk=pk)
    game.can_edit_or_403(request.user)
    form = GameForm(request.POST or None, instance=game)
    if form.is_valid():
        form.save()
        return redirect('game_list')
    return render(request, template_name, {'form': form})


def game_delete(request, pk, template_name='games/confirm_delete.html'):
    game = get_object_or_404(Game, pk=pk)
    game.can_edit_or_403(request.user)
    if request.method == 'POST':
        game.delete()
        return redirect('game_list')
    return render(request, template_name, {'object': game})


def game_next_status(request, pk):
    # TODO: Add javascript confirm button to template file
    game = get_object_or_404(Game, pk=pk)
    game.can_edit_or_403(request.user)
    try:
        game.next_status()
    except ValidationError as e:
        messages.error(request, e.message)
    return redirect('game_view', pk)


def game_previous_status(request, pk):
    # TODO: Add javascript confirm button to template file
    game = get_object_or_404(Game, pk=pk)
    game.can_edit_or_403(request.user)
    game.previous_status()
    return redirect('game_view', pk)


def game_signup(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.user == game.game_master:
        # Don't let game master register for their own game...
        return redirect('game_view', pk)
    signup = GameSignup.objects.filter(game=game, user=request.user).first()
    if signup is None:
        signup = GameSignup()
    signup.game = game
    signup.user = request.user
    if signup.can_signup():
        try:
            signup.status = signup.REGISTERED
            signup.save()
            game.signups.add(signup)
        except IntegrityError:
            pass
    return redirect('game_view', pk)


def game_withdraw(request, pk):
    game = get_object_or_404(Game, pk=pk)
    signup = get_object_or_404(GameSignup, game=game, user=request.user)
    if signup.can_withdraw():
        signup.status = signup.WITHDRAWN
        signup.save()
    return redirect('game_view', pk)


def game_signup_accept(request, pk):
    signup = get_object_or_404(GameSignup, pk=pk)
    signup.game.can_edit_or_403(request.user)
    if signup.can_accept():
        signup.status = signup.ACCEPTED
        signup.save()
    return redirect('game_view', signup.game.id)


def game_signup_reject(request, pk):
    signup = get_object_or_404(GameSignup, pk=pk)
    signup.game.can_edit_or_403(request.user)
    if signup.can_reject():
        signup.status = signup.REJECTED
        signup.save()
    return redirect('game_view', signup.game.id)
