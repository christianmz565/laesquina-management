const DEPLOY = true;

export let API_URL = "http://localhost:8000/api";
if (DEPLOY) {
    API_URL = "/api";
} 
