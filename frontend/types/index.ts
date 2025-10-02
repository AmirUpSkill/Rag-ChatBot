import { z } from "zod";

// --- User Schema & Type --- 
export const UserSchema = z.object({
    id: z.string(),
    email: z.string().email(),
    name: z.string().nullable(),
    avatar_url: z.string().url().nullable(),
    provider: z.string().nullable(),
    created_at: z.string().datetime().nullable(),
    role: z.string().default("user"),
});
export type User = z.infer<typeof UserSchema>;

// --- Auth State --- 
export interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;
}

// --- API Response Types --- 
export const SessionResponseSchema = z.object({
    success: z.boolean(),
    user: UserSchema,
})
export const LoginResponseSchema = z.object({
    success: z.boolean(),
    redirect_url: z.string().url(),
})

export const LogoutResponseSchema = z.object({
    success: z.boolean(),
    message: z.string(),
})
export type SessionResponse = z.infer<typeof SessionResponseSchema>;
export type LoginResponse = z.infer<typeof LoginResponseSchema>;
export type LogoutResponse = z.infer<typeof LogoutResponseSchema>;