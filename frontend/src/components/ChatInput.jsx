import { useRef } from "react";
import clsx from "clsx";

const ChatInput = ({
  value,
  onChange,
  onSend,
  disabled,
  attachments,
  onUpload,
  onRemove,
}) => {
  const fileRef = useRef(null);

  const tooltip = disabled
    ? "Indexing documents… Please wait"
    : "Ask a question";

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div
        className={clsx(
          "rounded-2xl px-4 py-3 flex flex-col gap-2 shadow-xl transition-all",
          disabled ? "bg-[#262626]" : "bg-[#2f2f2f]"
        )}
        title={tooltip}
      >
        {/* Attachment chips */}
        {attachments.length > 0 && (
          <div className="flex gap-2 flex-wrap">
            {attachments.map((file, idx) => (
              <div
                key={idx}
                className="flex items-center gap-2 bg-[#3a3a3a] px-3 py-1.5 rounded-lg"
              >
                <span className="text-xs text-white truncate max-w-[160px]">
                  {file.name}
                </span>
                <button
                  onClick={() => onRemove(idx)}
                  className="text-red-400 hover:text-red-300"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="flex items-center gap-3">
          <button
            onClick={() => !disabled && fileRef.current.click()}
            className={clsx(
              "text-xl transition",
              disabled
                ? "text-gray-600 cursor-not-allowed"
                : "text-gray-400 hover:text-white"
            )}
            title="Upload document"
            disabled={disabled}
          >
            +
          </button>

          <input
            ref={fileRef}
            type="file"
            accept=".pdf,.docx,.txt"
            multiple
            hidden
            onChange={onUpload}
          />

          <input
            value={value}
            onChange={onChange}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !disabled) onSend();
            }}
            disabled={disabled}
            placeholder={
              disabled ? "Indexing documents…" : "Ask anything"
            }
            className="flex-1 bg-transparent outline-none text-white placeholder-gray-400 disabled:cursor-not-allowed"
          />

          <button
            onClick={onSend}
            disabled={disabled}
            className={clsx(
              "rounded-full w-9 h-9 flex items-center justify-center transition",
              disabled
                ? "bg-blue-600/40 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-500"
            )}
          >
            ↑
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
