/* eslint-disable @typescript-eslint/no-explicit-any */
import type { APIResponse } from "@/types/api";

export const useApi = () => {
  const config = useRuntimeConfig();
  const baseURL = config.public.apiBase || "http://localhost:8000";

  const handleResponse = async <T>(response: Response): Promise<APIResponse<T>> => {
    if (!response.ok) {
      const error = await response.json();
      return { error: { message: error.detail || "An error occurred", details: error } };
    }
    const data = await response.json();
    return { data };
  };

  const fetchWrapper = async <T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<APIResponse<T>> => {
    try {
      const response = await fetch(`${baseURL}${endpoint}`, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options.headers
        }
      });
      return handleResponse<T>(response);
    } catch (error) {
      return {
        error: {
          message: "Network error occurred",
          details: error
        }
      };
    }
  };

  return {
    get: <T>(endpoint: string) => fetchWrapper<T>(endpoint),
    post: <T>(endpoint: string, data: any) =>
      fetchWrapper<T>(endpoint, {
        method: "POST",
        body: JSON.stringify(data)
      }),
    put: <T>(endpoint: string, data: any) =>
      fetchWrapper<T>(endpoint, {
        method: "PUT",
        body: JSON.stringify(data)
      }),
    patch: <T>(endpoint: string, data: any) =>
      fetchWrapper<T>(endpoint, {
        method: "PATCH",
        body: JSON.stringify(data)
      }),
    delete: <T>(endpoint: string, data?: any) =>
      fetchWrapper<T>(endpoint, {
        method: "DELETE",
        body: JSON.stringify(data)
      })
  };
};
