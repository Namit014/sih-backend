"use client";

import SearchForm from "@/components/SearchForm";
import AnalysisResults from "@/components/AnalysisResults";
import { useState } from "react";
import { AlertCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any | null>(null);

  const handleSearch = async (username: string) => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username }),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.detail || result.message || "Failed to analyze account");
      }

      setData(result);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen py-16 px-4 md:px-8 flex flex-col items-center selection:bg-primary/30 relative">
      <div className="absolute top-0 w-full h-[500px] bg-gradient-to-b from-primary/10 to-transparent pointer-events-none -z-10"></div>
      
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: "easeOut" }}
        className="text-center mb-12 mt-10"
      >
        <div className="inline-block mb-4 px-4 py-1.5 rounded-full border border-primary/30 bg-primary/10 text-primary text-sm font-medium tracking-wide">
          Advanced Threat Intelligence
        </div>
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white via-gray-200 to-gray-500">
          X Account Risk Detection
        </h1>
        <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto font-light leading-relaxed">
          Uncover anomalous behavioral patterns and evaluate the authenticity of public accounts using deep feature analysis.
        </p>
      </motion.div>

      <div className="w-full relative z-10">
        <SearchForm onSearch={handleSearch} isLoading={loading} />
      </div>

      <AnimatePresence mode="wait">
        {error && (
          <motion.div 
            key="error"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-8 p-4 bg-red-500/10 border border-red-500/20 rounded-2xl flex items-center gap-3 text-red-400 max-w-2xl w-full"
          >
            <AlertCircle size={20} />
            <p>{error}</p>
          </motion.div>
        )}

        {data && !loading && (
          <motion.div key="results" className="w-full">
            <AnalysisResults data={data} />
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
