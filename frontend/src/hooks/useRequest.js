import { useApiClient } from "@/services/api";
import { ref } from "vue";

export function useRequest() {
  const data = ref(null);
  const loading = ref(false);
  const api = useApiClient()

  const requestGet = async (url, params = {}) => {
    loading.value = true;
    try {
      const response = await api.get(url, params)
      data.value = response.data;
    } catch (e) {
      console.log(e);
    } finally {
      console.log("Success fetched!");
      loading.value = false;
    }
  };

  const requestPost = async (url, itemObj = {}) => {
    loading.value = true;
    try {
      const response = await api.post(url, itemObj);
    } catch (e) {
      console.log(e);
    } finally {
      console.log("Success posted!");
      loading.value = false;
    }
  };

  return {
    data,
    loading,
    requestGet,
    requestPost
  };
}
