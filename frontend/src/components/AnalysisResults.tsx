"use client";

import { motion } from "framer-motion";
import { User, Users, Calendar, MessageSquare, AlertTriangle, Sparkles, CheckCircle } from "lucide-react";
import RiskMeter from "./RiskMeter";

// Interface matches our FastAPI response schema
interface AnalysisData {
  account: {
    id: string;
    username: string;
    name: string;
    description?: string;
    created_at: string;
    profile_image_url?: string;
    followers: number;
    following: number;
    posts: number;
    verified: boolean;
  };
  risk: {
    score: number;
    probability: number;
    level: string;
  };
  signals: string[];
  explanation?: string;
}

export default function AnalysisResults({ data }: { data: AnalysisData }) {
  const { account, risk, signals, explanation } = data;

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.2 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
  };

  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="w-full max-w-5xl mx-auto mt-12 grid grid-cols-1 lg:grid-cols-3 gap-8"
    >
      {/* Left Column: Account Info */}
      <motion.div variants={itemVariants} className="col-span-1 glass-panel rounded-3xl p-8 flex flex-col items-center text-center">
        <div className="relative w-28 h-28 mb-6">
          {account.profile_image_url ? (
            <img 
              src={account.profile_image_url.replace('_normal', '_400x400')} 
              alt={account.name} 
              className="rounded-full w-full h-full object-cover border-4 border-card shadow-xl"
            />
          ) : (
            <div className="w-full h-full rounded-full bg-gray-800 flex items-center justify-center border-4 border-card">
              <User size={48} className="text-gray-500" />
            </div>
          )}
          {account.verified && (
            <div className="absolute bottom-0 right-0 bg-blue-500 text-white p-1.5 rounded-full border-2 border-card">
              <CheckCircle size={16} />
            </div>
          )}
        </div>
        
        <h2 className="text-2xl font-bold text-foreground mb-1">{account.name}</h2>
        <p className="text-primary font-medium mb-4">@{account.username}</p>
        
        {account.description && (
          <p className="text-gray-400 text-sm mb-6 leading-relaxed">{account.description}</p>
        )}
        
        <div className="w-full grid grid-cols-2 gap-4 mt-auto border-t border-border pt-6">
          <div className="flex flex-col items-center">
            <span className="text-gray-500 text-xs uppercase font-semibold flex items-center gap-1 mb-1">
              <Users size={12} /> Followers
            </span>
            <span className="text-foreground font-bold">{account.followers.toLocaleString()}</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-gray-500 text-xs uppercase font-semibold flex items-center gap-1 mb-1">
              <User size={12} /> Following
            </span>
            <span className="text-foreground font-bold">{account.following.toLocaleString()}</span>
          </div>
          <div className="flex flex-col items-center mt-2">
            <span className="text-gray-500 text-xs uppercase font-semibold flex items-center gap-1 mb-1">
              <MessageSquare size={12} /> Posts
            </span>
            <span className="text-foreground font-bold">{account.posts.toLocaleString()}</span>
          </div>
          <div className="flex flex-col items-center mt-2">
            <span className="text-gray-500 text-xs uppercase font-semibold flex items-center gap-1 mb-1">
              <Calendar size={12} /> Joined
            </span>
            <span className="text-foreground font-bold text-sm">{formatDate(account.created_at)}</span>
          </div>
        </div>
      </motion.div>

      {/* Right Column: Risk & Signals */}
      <div className="col-span-1 lg:col-span-2 flex flex-col gap-8">
        
        <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <RiskMeter score={risk.score} level={risk.level} />
          
          <div className="glass-panel rounded-3xl p-6 flex flex-col">
            <h3 className="text-gray-400 font-medium tracking-wider text-sm uppercase mb-4 flex items-center gap-2">
              <AlertTriangle size={16} className="text-orange-500" /> Detected Signals
            </h3>
            <div className="flex-1 overflow-y-auto pr-2">
              {signals.length > 0 ? (
                <ul className="space-y-3">
                  {signals.map((signal, idx) => (
                    <motion.li 
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 1 + (idx * 0.1) }}
                      key={idx} 
                      className="bg-card/50 border border-border/50 p-3 rounded-xl text-sm flex items-start gap-3"
                    >
                      <div className="mt-0.5 min-w-[8px] h-2 rounded-full bg-orange-500"></div>
                      <span className="text-gray-300">{signal}</span>
                    </motion.li>
                  ))}
                </ul>
              ) : (
                <div className="h-full flex items-center justify-center text-gray-500 text-sm">
                  No anomalous signals detected.
                </div>
              )}
            </div>
          </div>
        </motion.div>

        {explanation && (
          <motion.div variants={itemVariants} className="glass-panel rounded-3xl p-6 relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <h3 className="text-gray-400 font-medium tracking-wider text-sm uppercase mb-4 flex items-center gap-2 relative z-10">
              <Sparkles size={16} className="text-primary" /> AI Explanation
            </h3>
            <p className="text-gray-300 leading-relaxed relative z-10 text-sm md:text-base">
              {explanation}
            </p>
          </motion.div>
        )}
        
      </div>
    </motion.div>
  );
}
