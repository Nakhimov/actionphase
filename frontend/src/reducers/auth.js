import jwtDecode from 'jwt-decode'
import * as auth from '../actions/auth'

const initialState = {
    access: undefined,
    fetching: false,
    errors: {},
};

const authReducer = (state = initialState, action) => {
    switch (action.type) {
        case auth.LOGIN_SUCCESS:
        case auth.REGISTRATION_SUCCESS:
            return {
                access: {
                    token: action.payload.token,
                    ...jwtDecode(action.payload.token)
                },
                errors: {}
            };
        case auth.LOGIN_REQUEST:
        case auth.REGISTRATION_REQUEST:
        case auth.TOKEN_REQUEST:
            return {
                fetching: true
            };
        case auth.TOKEN_RECEIVED:
            return {
                ...state,
                access: {
                    token: action.payload.token,
                    ...jwtDecode(action.payload.token)
                },
                fetching: false
            };
        case auth.LOGIN_FAILURE:
        case auth.REGISTRATION_FAILURE:
        case auth.TOKEN_FAILURE:
            return {
                access: undefined,
                fetching: false,
                errors:
                action.payload.response ||
                {'non_field_errors': action.payload.statusText},
            };
        default:
            return state
    }
};

export default authReducer;