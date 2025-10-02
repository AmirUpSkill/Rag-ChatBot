import { z } from "zod";
import {
  UserSchema,
  SessionResponseSchema,
  LogoutResponseSchema,
  type User,
  type SessionResponse,
  type LogoutResponse,
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message);
    this.name = "APIError";
  }
}

class APIClient {
  private readonly baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    schema?: z.ZodSchema<T>
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new APIError(
        errorData.detail || errorData.message || "Request failed",
        response.status,
        errorData.code
      );
    }

    const data = await response.json();

    // ---  Validate response with Zod if schema provided ---
    if (schema) {
      try {
        return schema.parse(data);
      } catch (error) {
        if (error instanceof z.ZodError) {
          console.error("API Response validation error:", error.issues);
          throw new APIError("Invalid response format", 500);
        }
        throw error;
      }
    }

    return data;
  }

  // --- Auth Endpoints ---

  async getCurrentUser(): Promise<User> {
    return this.request("/api/v1/auth/me", {}, UserSchema);
  }

  async createSession(
    accessToken: string,
    refreshToken: string
  ): Promise<SessionResponse> {
    return this.request(
      "/api/v1/auth/session",
      {
        method: "POST",
        body: JSON.stringify({
          access_token: accessToken,
          refresh_token: refreshToken,
        }),
      },
      SessionResponseSchema
    );
  }

  async logout(): Promise<LogoutResponse> {
    return this.request(
      "/api/v1/auth/logout",
      {
        method: "POST",
      },
      LogoutResponseSchema
    );
  }

  async refreshToken(): Promise<void> {
    await this.request("/api/v1/auth/refresh", {
      method: "POST",
    });
  }

  // --- Helper to get Google login URL ---
  getGoogleLoginURL(): string {
    return `${this.baseURL}/api/v1/auth/login/google`;
  }
}

export const apiClient = new APIClient(API_BASE_URL);
export { APIError };