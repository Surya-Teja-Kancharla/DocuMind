const WelcomePanel = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-white px-4">
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold tracking-tight">
          Welcome to <span className="text-blue-500">DocuMind</span>
        </h1>
        {/* Removed "Upload document to begin" line as requested */}
        <p className="text-slate-400 text-lg font-medium">
          How can I help you today?
        </p>
      </div>

      <div className="absolute bottom-24 w-full text-center">
        <p className="text-[11px] text-slate-500 uppercase tracking-widest">
          AI can make mistakes. Please double-check important information.
        </p>
      </div>
    </div>
  );
};

export default WelcomePanel;
