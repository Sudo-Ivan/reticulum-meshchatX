import axios from 'axios';
import { createApp } from 'vue';
import "./style.css";
import CallPage from "./components/call/CallPage.vue";
import { ensureCodec2ScriptsLoaded } from "./js/Codec2Loader";

// provide axios globally
window.axios = axios;

async function bootstrap() {
    await ensureCodec2ScriptsLoaded();
    createApp(CallPage)
        .mount('#app');
}

bootstrap();
