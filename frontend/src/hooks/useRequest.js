import { useApiClient } from "@/services/api";
import { ref, reactive, toRaw } from "vue";

export function useRequest() {
  const data = ref(null);
  const loading = ref(false);
  const api = useApiClient()

  const requestGet = async (url, params = {}) => {
    loading.value = true;
    let respData;
    try {
      const response = await api.get(url, params)
      respData = response.data;
      data.value = respData;
    } catch (e) {
      console.log(e);
    } finally {
      console.log("Success fetched!");
      loading.value = false;
    }
    return respData;
  };

  const requestPost = async (url, itemObj = {}) => {
    loading.value = true;
        let respData;
    try {
      const response = await api.post(url, itemObj,   {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
            respData = response.data;
      data.value = respData;
    } catch (e) {
      console.log(e);
    } finally {
      console.log("reg posted!");
      loading.value = false;
    }

    return respData;
  };

  return {
    data,
    loading,
    requestGet,
    requestPost
  };
}
