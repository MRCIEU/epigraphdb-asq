export let web_backend_url: string | null = "";

if (process.env.VUE_APP_WEB_BACKEND_URL) {
  web_backend_url = `${process.env.VUE_APP_WEB_BACKEND_URL}`;
} else {
  web_backend_url = null;
  console.error("web_backend_url not set!");
}
