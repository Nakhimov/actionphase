import { RSAA } from 'redux-api-middleware';
import {withAuth} from "../util/api";
export const GAME_LIST_REQUEST = '@@games/GAME_LIST_REQUEST';
export const GAME_LIST_SUCCESS = '@@games/GAME_LIST_SUCCESS';
export const GAME_LIST_FAILURE = '@@games/GAME_LIST_FAILURE';

export const GAME_DETAIL_REQUEST = '@@games/GAME_DETAIL_REQUEST';
export const GAME_DETAIL_SUCCESS = '@@games/GAME_DETAIL_SUCCESS';
export const GAME_DETAIL_FAILURE = '@@games/GAME_DETAIL_FAILURE';


export const gameList = () => ({
  [RSAA]: {
      endpoint: 'http://192.168.99.100:8000/api/games/',
      method: 'GET',
      headers: withAuth({ 'Content-Type': 'application/json' }),
      types: [
        GAME_LIST_REQUEST, GAME_LIST_SUCCESS, GAME_LIST_FAILURE
      ]
  }
});

export const gameDetail = (id) => ({
  [RSAA]: {
      endpoint: 'http://192.168.99.100:8000/api/games/' + id + '/',
      method: 'GET',
      headers: withAuth({ 'Content-Type': 'application/json' }),
      types: [
        GAME_DETAIL_REQUEST, GAME_DETAIL_SUCCESS, GAME_DETAIL_FAILURE
      ]
  }
});