const Trending = ({ trends, fetchCritique}: { trends: string[], fetchCritique: (website: string) => void }) => {
  return (
    <div className="m-auto w-auto h-auto text-gray-100 leading-7 rounded-[20px] bg-slate-700 p-5">
      <h2 className="text-[20px] text-white font-bold">Trending💫</h2>
      <ul>
        {trends.length > 0 ? (
          trends.map((website, index) => (
            <li key={index} className="border-b last:border-b-0">
              <button 
                className="p-1 text-gray-100 hover:text-gray-400" 
                onClick={() => fetchCritique(website)}>
                  {website}
              </button>
            </li>
          ))
        ) : (
          <li className="p-4 text-gray-500">No trending websites available.</li>
        )}
      </ul>
    </div>
  );
};

export default Trending;
