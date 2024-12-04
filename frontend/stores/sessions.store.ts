import { defineStore } from "pinia";
import { ref } from "vue";
import type { UUID } from "crypto";
import type { Session, SessionCreate, SessionDetail, SessionUpdate } from "@/types/api";
import { useSession } from "@/composables/useSession";

export const useSessionStore = defineStore("session", () => {
  // State
  const sessions = ref<Session[]>([]);
  const currentSession = ref<Session | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const sessionApi = useSession();

  // Actions
  const fetchSessions = async () => {
    isLoading.value = true;
    error.value = null;

    const response = await sessionApi.getSessions();

    if (response.error) {
      error.value = response.error.message;
    } else {
      sessions.value = response.data || [];
    }

    isLoading.value = false;
  };

  const fetchSession = async (id: UUID) => {
    isLoading.value = true;
    error.value = null;

    const response = await sessionApi.getSession(id);

    if (response.error) {
      error.value = response.error.message;
    } else {
      currentSession.value = response.data as SessionDetail;
    }

    isLoading.value = false;
  };

  const createSession = async (sessionData: SessionCreate) => {
    isLoading.value = true;
    error.value = null;

    const response = await sessionApi.createSession(sessionData);

    if (response.error) {
      error.value = response.error.message;
    } else {
      currentSession.value = response.data as Session;
      sessions.value.push(response.data as Session);
    }

    isLoading.value = false;
  };

  const updateSession = async (id: UUID, sessionData: SessionUpdate) => {
    isLoading.value = true;
    error.value = null;

    const response = await sessionApi.updateSession(id, sessionData);

    if (response.error) {
      error.value = response.error.message;
    } else {
      const updatedSession = response.data as Session;
      currentSession.value = updatedSession;
      const index = sessions.value.findIndex((s) => s.id === id);
      if (index !== -1) {
        sessions.value[index] = updatedSession;
      }
    }

    isLoading.value = false;
  };

  const deleteSession = async (id: UUID) => {
    isLoading.value = true;
    error.value = null;

    const response = await sessionApi.deleteSession(id);

    if (response.error) {
      error.value = response.error.message;
    } else {
      if (currentSession.value?.id === id) {
        currentSession.value = null;
      }
      sessions.value = sessions.value.filter((s) => s.id !== id);
    }

    isLoading.value = false;
  };

  return {
    // State
    sessions,
    currentSession,
    isLoading,
    error,
    // Actions
    fetchSessions,
    fetchSession,
    createSession,
    updateSession,
    deleteSession
  };
});
