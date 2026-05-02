import { ChatInterface } from "@/components/ChatInterface";
import { Header } from "@/components/Header";

export default function HomePage() {
  return (
    <main className="min-h-screen px-4 py-8">
      <div className="mx-auto max-w-4xl space-y-8">
        <Header />
        <ChatInterface />
      </div>
    </main>
  );
}
