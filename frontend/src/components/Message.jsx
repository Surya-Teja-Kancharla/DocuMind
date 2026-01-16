import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import clsx from "clsx";

const Message = ({ role, content, isStreaming = false }) => {
  const isUser = role === "user";
  const isSystemError =
    role === "assistant" && content?.trim().startsWith("⚠️");

  return (
    <div
      className={clsx(
        "w-full flex mb-4",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={clsx(
          "max-w-[70%] rounded-xl px-4 py-3 text-sm leading-relaxed relative overflow-hidden",
          isUser && "bg-blue-600 text-white",
          !isUser && !isSystemError &&
            "bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100",
          isSystemError &&
            "bg-yellow-50 text-yellow-800 border border-yellow-300 dark:bg-yellow-900/20 dark:text-yellow-200"
        )}
      >
        {isStreaming && !isSystemError && (
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-pulse" />
        )}

        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>

        {isStreaming && !isSystemError && (
          <span className="inline-block ml-1 animate-pulse">▍</span>
        )}
      </div>
    </div>
  );
};

export default Message;
