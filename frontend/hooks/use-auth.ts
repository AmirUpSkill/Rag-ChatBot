import { useAuthStore } from "@/lib/store/auth-store";
import { apiClient, APIError } from "@/lib/api";
import { useCallback } from "react";

export function useAuth() {
  const { user, isAuthenticated, isLoading, error, setUser, setLoading, setError, clearAuth } =
    useAuthStore();

  const fetchUser = useCallback(async () => {
    try {
      setLoading(true);
      const userData = await apiClient.getCurrentUser();
      setUser(userData);
    } catch (error) {
      if (error instanceof APIError && error.status === 401) {
        clearAuth();
      } else {
        setError(error instanceof Error ? error.message : "Failed to fetch user");
      }
    }
  }, [setUser, setLoading, setError, clearAuth]);

  const logout = useCallback(async () => {
    try {
      await apiClient.logout();
      clearAuth();
      window.location.href = "/";
    } catch (error) {
      clearAuth();
      window.location.href = "/";
    }
  }, [clearAuth]);

  const loginWithGoogle = useCallback(() => {
    window.location.href = apiClient.getGoogleLoginURL();
  }, []);

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    fetchUser,
    logout,
    loginWithGoogle,
  };
}