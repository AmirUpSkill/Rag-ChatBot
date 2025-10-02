import { Header } from "@/components/shared/header";
import { Button } from "@/components/ui/button";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <Header />

      {/* Hero Section */}
      <main className="flex-1 flex items-center justify-center">
        <div className="container mx-auto px-6 py-20 text-center max-w-4xl">
          <h2 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
            Chat with Your Documents
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Upload any PDF and have intelligent conversations powered by advanced AI. 
            Get instant answers from your documents with RAG technology.
          </p>
          <div className="flex gap-4 justify-center">
            <Button size="lg" className="bg-brand hover:bg-brand-hover text-white">
              Start Now for Free
            </Button>
            <Button size="lg" variant="outline">
              Watch Demo
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}