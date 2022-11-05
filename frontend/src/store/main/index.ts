import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { MainState } from './state';

const defaultState: MainState = {
  isLoggedIn: null,
  token: '',
  logInError: false,
  registerError: false,
  userProfile: null,
  dashboardShowDrawer: true,
  notifications: [],
  darkTheme: false,
};

export const mainModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
