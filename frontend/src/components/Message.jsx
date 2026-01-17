import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import clsx from "clsx";

const Message = ({ role, content, isStreaming = false }) => {
  const isUser = role === "user";
  const isSystemError = role === "assistant" && content?.trim().startsWith("⚠️");

  return (
    <div className={clsx("w-full flex mb-6", isUser ? "justify-end" : "justify-start")}>
      <div
        className={clsx(
          "max-w-[85%] rounded-2xl px-6 py-4 relative overflow-hidden transition-all duration-200",
          isUser && "bg-blue-600 text-white shadow-lg",
          !isUser && !isSystemError && "bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100 shadow-md",
          isSystemError && "bg-yellow-50 text-yellow-900 border border-yellow-300"
        )}
      >
        <div className="relative z-10 prose prose-slate dark:prose-invert max-w-none">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              h1: ({ node, ...props }) => (
                <h1 className="text-2xl font-bold mb-3 mt-2 pb-2 border-b-2 border-blue-500" {...props} />
              ),
              h2: ({ node, ...props }) => (
                <h2 className="text-xl font-bold mb-3 mt-4" {...props} />
              ),
              h3: ({ node, ...props }) => (
                <h3 className="text-lg font-semibold mb-2 mt-3" {...props} />
              ),
              p: ({ node, ...props }) => (
                <p className="mb-3 leading-7 text-[15px]" {...props} />
              ),
              ul: ({ node, ...props }) => (
                <ul className="space-y-1.5 mb-3 ml-0 list-none" {...props} />
              ),
              ol: ({ node, ...props }) => (
                <ol className="space-y-1.5 mb-3 ml-6 list-decimal" {...props} />
              ),
              li: ({ node, children, ...props }) => {
                const parent = node.parent;
                const isUnordered = parent?.type === 'element' && parent.tagName === 'ul';
                
                return isUnordered ? (
                  <li className="flex items-start leading-7" {...props}>
                    <span className="text-blue-500 font-bold mr-2.5 mt-0.5 flex-shrink-0">•</span>
                    <span className="flex-1">{children}</span>
                  </li>
                ) : (
                  <li className="leading-7" {...props}>{children}</li>
                );
              },
              strong: ({ node, ...props }) => (
                <strong className="font-bold text-slate-900 dark:text-white" {...props} />
              ),
              em: ({ node, ...props }) => (
                <em className="italic" {...props} />
              ),
              a: ({ node, ...props }) => (
                <a
                  className="text-blue-600 hover:text-blue-800 underline dark:text-blue-400"
                  target="_blank"
                  rel="noopener noreferrer"
                  {...props}
                />
              ),
              code: ({ node, inline, className, children, ...props }) => {
                return inline ? (
                  <code
                    className={clsx(
                      "px-1.5 py-0.5 rounded text-sm font-mono",
                      isUser ? "bg-blue-700 text-blue-100" : "bg-slate-200 text-red-600 dark:bg-slate-700 dark:text-red-400"
                    )}
                    {...props}
                  >
                    {children}
                  </code>
                ) : (
                  <div className="my-3 rounded-lg overflow-hidden bg-slate-900">
                    <pre className="p-4 overflow-x-auto text-sm">
                      <code className="text-green-400 font-mono" {...props}>
                        {children}
                      </code>
                    </pre>
                  </div>
                );
              },
              blockquote: ({ node, ...props }) => (
                <blockquote
                  className="border-l-4 border-blue-500 pl-4 py-1 my-3 italic text-slate-600 dark:text-slate-400"
                  {...props}
                />
              ),
              table: ({ node, ...props }) => (
                <div className="overflow-x-auto my-3">
                  <table className="min-w-full border-collapse" {...props} />
                </div>
              ),
              thead: ({ node, ...props }) => (
                <thead className="bg-slate-200 dark:bg-slate-700" {...props} />
              ),
              th: ({ node, ...props }) => (
                <th className="border border-slate-300 dark:border-slate-600 px-3 py-2 text-left font-semibold" {...props} />
              ),
              td: ({ node, ...props }) => (
                <td className="border border-slate-300 dark:border-slate-600 px-3 py-2" {...props} />
              ),
              hr: ({ node, ...props }) => (
                <hr className="my-4 border-t border-slate-300 dark:border-slate-600" {...props} />
              ),
            }}
          >
            {content}
          </ReactMarkdown>
        </div>

        {isStreaming && !isSystemError && (
          <span className="inline-block ml-1 w-0.5 h-5 bg-blue-500 animate-pulse">▋</span>
        )}
      </div>
    </div>
  );
};

export default Message;