import type { UUID } from "crypto";
import { useApi } from "@/composables/useApi";
import type { Chain, AvailableChain, ChainSelection } from "@/types/api";

export const useChain = () => {
  const api = useApi();

  const getAvailableChains = () => api.get<AvailableChain[]>("/available-chains");

  const selectChains = (sessionId: UUID, data: ChainSelection) =>
    api.post<Chain[]>(`/sessions/${sessionId}/select-chains`, data);

  // TODO: Add getSessionChains and deleteSessionChains

  const getChains = (sessionId: UUID) => api.get<Chain[]>(`/sessions/${sessionId}/chains`);

  const deleteChain = (sessionId: UUID, chainId: UUID) =>
    api.delete<Chain>(`/sessions/${sessionId}/chains/${chainId}`);

  return {
    getAvailableChains,
    selectChains,
    getChains,
    deleteChain
  };
};
