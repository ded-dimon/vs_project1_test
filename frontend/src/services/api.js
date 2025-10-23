import { useAppStore } from "@/store/app"
import axios from "axios"

const apiClient = axios.create({
    timeout: 10000,
    params: {}
})

export const useApiClient = () => {
    const appStore = useAppStore()

    if(appStore.baseUrlServer){
        apiClient.defaults.baseURL = appStore.baseUrlServer
    }

    return apiClient
}