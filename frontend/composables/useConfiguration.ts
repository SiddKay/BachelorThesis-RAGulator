import type { UUID } from "crypto";
import { useApi } from "@/composables/useApi";
import type { Configuration, ConfigurationCreate, ConfigurationUpdate } from "@/types/api";

export const useConfiguration = () => {
  const api = useApi();

  const getConfiguration = (sessionId: UUID, configId: UUID) =>
    api.get<Configuration>(`/sessions/${sessionId}/configurations/${configId}`);

  const getAllConfigurations = (sessionId: UUID) =>
    api.get<Configuration[]>(`/sessions/${sessionId}/configurations`);

  const getAverageScoreOfConfiguration = (configId: UUID) =>
    api.get<number>(`/configurations/${configId}/score`);

  const createConfiguration = (sessionId: UUID, data: ConfigurationCreate) =>
    api.post<Configuration>(`/sessions/${sessionId}/configurations`, data);

  const updateConfiguration = (sessionId: UUID, configId: UUID, data: ConfigurationUpdate) =>
    api.patch<Configuration>(`/sessions/${sessionId}/configurations/${configId}`, data);

  const deleteConfiguration = (sessionId: UUID, configId: UUID) =>
    api.delete<Configuration>(`/sessions/${sessionId}/configurations/${configId}`);

  return {
    getConfiguration,
    getAllConfigurations,
    getAverageScoreOfConfiguration,
    createConfiguration,
    updateConfiguration,
    deleteConfiguration
  };
};
