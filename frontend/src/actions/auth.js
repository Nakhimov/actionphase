import { RSAA } from 'redux-api-middleware'

export const REGISTRATION_REQUEST = '@@auth/REGISTRATION_REQUEST';
export const REGISTRATION_SUCCESS = '@@auth/REGISTRATION_SUCCESS';
export const REGISTRATION_FAILURE = '@@auth/REGISTRATION_FAILURE';
export const LOGIN_REQUEST = '@@auth/LOGIN_REQUEST';
export const LOGIN_SUCCESS = '@@auth/LOGIN_SUCCESS';
export const LOGIN_FAILURE = '@@auth/LOGIN_FAILURE';
export const TOKEN_REQUEST = '@@auth/TOKEN_REQUEST';
export const TOKEN_RECEIVED = '@@auth/TOKEN_RECEIVED';
export const TOKEN_FAILURE = '@@auth/TOKEN_FAILURE';

export const register = (username, password1, password2, email) => ({
  [RSAA]: {
    endpoint: 'http://192.168.99.100:8000/api/auth/registration/',
    method: 'POST',
    body: JSON.stringify({username, password1, password2, email}),
    headers: { 'Content-Type': 'application/json' },
    types: [
      REGISTRATION_REQUEST, REGISTRATION_SUCCESS, REGISTRATION_FAILURE
    ]
  }
});

export const login = (username, password) => ({
  [RSAA]: {
    endpoint: 'http://192.168.99.100:8000/api/auth/login/',
    method: 'POST',
    body: JSON.stringify({username, password}),
    headers: { 'Content-Type': 'application/json' },
    types: [
      LOGIN_REQUEST, LOGIN_SUCCESS, LOGIN_FAILURE
    ]
  }
});

export const refreshAccessToken = (token) => ({
  [RSAA]: {
    endpoint: 'http://192.168.99.100:8000/api/auth/token/refresh/',
    method: 'POST',
    body: JSON.stringify({token: token}),
    headers: { 'Content-Type': 'application/json' },
    types: [
      TOKEN_REQUEST, TOKEN_RECEIVED, TOKEN_FAILURE
    ]
  }
});