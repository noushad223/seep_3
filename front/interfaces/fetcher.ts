import axiosClient from "./axiosClient";
import { axiosConfig } from "./axiosConfig";

const config = axiosConfig();
export const fetcher = (url) =>
    axiosClient(url, config)
        .then((response) => response.data)
        .catch((error) => {
            console.error("Error fetching data:", error);
            throw error;
        });

        