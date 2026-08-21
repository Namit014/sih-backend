"use client";

import { useState } from "react";
import { Search, Loader2 } from "lucide-react";
import { motion } from "framer-motion";

interface SearchFormProps {
  onSearch: (username: string) => void;
  isLoading: boolean;
}

export default function SearchForm({ onSearch, isLoading }: SearchFormProps) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSearch(input.trim());
    }
  };

  return (
    <motion.form 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      onSubmit={handleSubmit} 
      className="w-full max-w-2xl mx-auto"
    >
      <div className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-primary to-blue-400 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
        <div className="relative flex items-center bg-card border border-border rounded-2xl overflow-hidden shadow-2xl">
          <div className="pl-5 text-gray-400">
            <Search size={20} />
          </div>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter X @username or profile URL..."
            className="w-full bg-transparent border-none py-4 px-4 text-foreground placeholder:text-gray-500 focus:outline-none focus:ring-0 text-lg"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-8 py-4 bg-primary text-primary-foreground font-medium hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[120px]"
          >
            {isLoading ? <Loader2 className="animate-spin" size={20} /> : "Analyze"}
          </button>
        </div>
      </div>
    </motion.form>
  );
}
