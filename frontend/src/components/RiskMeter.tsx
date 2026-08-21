"use client";

import { motion } from "framer-motion";

interface RiskMeterProps {
  score: number;
  level: string;
}

export default function RiskMeter({ score, level }: RiskMeterProps) {
  // Determine color based on risk level
  let colorClass = "text-emerald-500";
  let bgClass = "bg-emerald-500/20";
  let strokeClass = "stroke-emerald-500";
  
  if (level.toLowerCase() === "moderate") {
    colorClass = "text-yellow-500";
    bgClass = "bg-yellow-500/20";
    strokeClass = "stroke-yellow-500";
  } else if (level.toLowerCase() === "suspicious") {
    colorClass = "text-orange-500";
    bgClass = "bg-orange-500/20";
    strokeClass = "stroke-orange-500";
  } else if (level.toLowerCase() === "high") {
    colorClass = "text-red-500";
    bgClass = "bg-red-500/20";
    strokeClass = "stroke-red-500";
  }

  // Calculate SVG circle properties
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-card border border-border rounded-3xl shadow-lg relative overflow-hidden">
      <div className={`absolute -top-10 -right-10 w-32 h-32 rounded-full blur-3xl opacity-20 ${bgClass.split('/')[0]}`}></div>
      
      <h3 className="text-gray-400 font-medium tracking-wider text-sm uppercase mb-6 z-10">Risk Score</h3>
      
      <div className="relative flex items-center justify-center mb-6 z-10">
        <svg className="transform -rotate-90 w-40 h-40">
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke="currentColor"
            strokeWidth="8"
            fill="transparent"
            className="text-gray-800"
          />
          <motion.circle
            cx="80"
            cy="80"
            r={radius}
            stroke="currentColor"
            strokeWidth="10"
            fill="transparent"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            className={strokeClass}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span 
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
            className={`text-5xl font-bold ${colorClass}`}
          >
            {score}
          </motion.span>
        </div>
      </div>
      
      <motion.div 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1, duration: 0.5 }}
        className={`px-4 py-1.5 rounded-full text-sm font-semibold tracking-wide uppercase ${bgClass} ${colorClass} z-10`}
      >
        {level} Risk
      </motion.div>
    </div>
  );
}
