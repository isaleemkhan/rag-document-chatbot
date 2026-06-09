"use client";

import { useState } from "react";
import FileUpload from "@/components/FileUpload";
import ChatWindow from "@/components/ChatWindow";

export default function Home() {
  const [uploadedDocs, setUploadedDocs] = useState<string[]>([]);

  return (
    <main className="min-h-screen bg-zinc-900 text-zinc-100 flex flex-col items-center p-6">
      <div className="w-full max-w-3xl flex flex-col gap-4" style={{ height: "calc(100vh - 48px)" }}>
        <header>
          <h1 className="text-2xl font-semibold tracking-tight">RAG Document Chatbot</h1>
          <p className="text-sm text-zinc-400 mt-1">Upload your docs and chat with them using GPT-4o</p>
        </header>

        <FileUpload
          onUploadSuccess={(name) => setUploadedDocs((prev) => [...prev, name])}
        />

        {uploadedDocs.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {uploadedDocs.map((doc) => (
              <span key={doc} className="text-xs bg-zinc-800 text-zinc-300 px-2 py-1 rounded-full">
                📄 {doc}
              </span>
            ))}
          </div>
        )}

        <div className="flex-1 rounded-2xl border border-zinc-700 overflow-hidden min-h-0">
          <ChatWindow />
        </div>
      </div>
    </main>
  );
}
