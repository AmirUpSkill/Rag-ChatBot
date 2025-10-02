"use client";

import { useEffect } from "react";
import { useAuth } from "@/hooks/use-auth";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const { fetchUser } = useAuth();

  useEffect(() => {
    // Check if user is already authenticated on app load
    fetchUser();
  }, [fetchUser]);

  return <>{children}</>;
}
