from django.test import TestCase
from houseoffun.houseoffun.models.games import *


class GamesTest(TestCase):
    """
    Test model functionality for the Games model
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_pass')
        self.game = Game.objects.create(
            name='Sample of Fun',
            abbreviation='SoF',
            description='This is a sample game!',
            game_master=self.user
        )

    def test_advance_to_registration(self):
        # Draft progresses to registration, but has no other effects
        self.assertEquals(Game.DRAFT, self.game.status)
        self.game.next_status()
        self.assertEquals(Game.REGISTRATION, self.game.status)

    def test_revert_draft_fails(self):
        # Draft cannot be reverted to a previous state
        self.assertEquals(Game.DRAFT, self.game.status)
        self.game.previous_status()
        self.assertEquals(Game.DRAFT, self.game.status)

    def test_revert_to_draft(self):
        # Reverting should reset to DRAFT status and destroy all signups
        self.game.status = Game.REGISTRATION
        # This is technically invalid, a user shouldn't be able to sign up for their own game
        signup = GameSignup.objects.create(user=self.user, game=self.game)
        self.game.previous_status()
        self.assertEquals(Game.DRAFT, self.game.status)
        signup = GameSignup.objects.filter(pk=signup.id).first()
        self.assertIsNone(signup)

    def test_advance_to_pending(self):
        # Advance to pending should only work if all registrations have been handled and should create characters
        self.game.status = Game.REGISTRATION
        signup = GameSignup.objects.create(user=self.user, game=self.game)
        with self.assertRaises(ValidationError):
            self.game.next_status()
        signup.status = GameSignup.ACCEPTED
        signup.save()
        self.game.next_status()
        self.assertEquals(Game.PENDING, self.game.status)
        character = Character.objects.filter(game=self.game, owner=self.user).first()
        self.assertIsNotNone(character)

    def test_revert_to_registration(self):
        # Reverting to registration should mark all characters deleted
        self.game.status = Game.PENDING
        character = Character.objects.create(game=self.game, owner=self.user)
        self.game.previous_status()
        character.refresh_from_db()
        self.assertEquals(Game.REGISTRATION, self.game.status)
        self.assertEquals(Character.DELETED,  character.status)
