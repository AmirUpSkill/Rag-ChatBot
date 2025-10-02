"use client";

import Link from "next/link";
import { useAuth } from "@/hooks/use-auth";
import { ThemeToggle } from "./theme-toggle";
import { UserAvatar } from "./user-avatar";
import { Button } from "@/components/ui/button";

export function Header() {
  const { isAuthenticated, loginWithGoogle } = useAuth();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center">
        <div className="mr-4 hidden md:flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="hidden font-bold sm:inline-block">RAG ChatBot</span>
          </Link>
        </div>
        
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <div className="w-full flex-1 md:w-auto md:flex-none">
            {/* Search or other components can go here */}
          </div>
          
          <nav className="flex items-center gap-2">
            <ThemeToggle />
            
            {isAuthenticated ? (
              <UserAvatar />
            ) : (
              <Button size="sm" onClick={loginWithGoogle} className="bg-brand hover:bg-brand-hover">
                Sign In
              </Button>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}
