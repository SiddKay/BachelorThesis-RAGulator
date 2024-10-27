import { defineStore } from "pinia";
import { ref } from "vue";

export const useConfigStore = defineStore("config", () => {
  const parameter1 = ref([50]);
  const parameter2 = ref([75]);
  const prompt = ref("");

  return {
    parameter1,
    parameter2,
    prompt
  };
});
