export type snackbarState = {
  color: string;
  visible: boolean;
  text: null | string;
  timeout: number;
};

type snackbarPayload = {
  text: string;
  color?: string;
};

const DEFAULT_COLOR = "blue-grey";

export const snackbar = {
  namespaced: true,
  state: (): snackbarState => ({
    color: DEFAULT_COLOR,
    visible: false,
    text: null,
    timeout: 6000,
  }),
  mutations: {
    showSnackbar(state: snackbarState, payload: snackbarPayload): void {
      state.text = payload.text;
      state.visible = true;
      if (payload.color == undefined) {
        state.color = DEFAULT_COLOR;
      } else {
        state.color = payload.color;
      }
    },
    closeSnackbar(state: snackbarState): void {
      state.visible = false;
      state.text = null;
    },
  },
};
