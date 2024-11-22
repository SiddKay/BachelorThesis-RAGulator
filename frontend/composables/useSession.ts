import type { UUID } from "crypto";
import { useRoute } from "vue-router";
import { useApi } from "@/composables/useApi";
import type { Session, SessionCreate, SessionDetail, SessionUpdate } from "@/types/api";

export const useSession = () => {
  const api = useApi();

  const getSession = (id: UUID) => api.get<SessionDetail>(`/sessions/${id}`);

  const getSessions = () => api.get<SessionDetail[]>("/sessions");

  const createSession = (data: SessionCreate) => api.post<Session>("/sessions", data);

  const updateSession = (id: UUID, data: SessionUpdate) =>
    api.patch<Session>(`/sessions/${id}`, data);

  const deleteSession = (id: UUID) => api.delete<Session>(`/sessions/${id}`);

  return {
    getSession,
    getSessions,
    createSession,
    updateSession,
    deleteSession
  };
};

export const useSessionContext = () => {
  const route = useRoute();

  const sessionId = computed(() => {
    const id = route.params.id;
    if (!id || Array.isArray(id)) {
      throw new Error("Invalid session ID");
    }
    return id as UUID;
  });

  return {
    sessionId
  };
};
