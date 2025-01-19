const Trending = ({ trends }: { trends: string[] }) => {
  return (
    <div className="m-auto w-auto h-auto text-red-400 leading-7 rounded-[20px] bg-gray-700 p-5">
      <h2 className="text-[20px] border-b">Trending💫</h2>
      <ul>
        {trends.length > 0 ? (
          trends.map((website, index) => <li key={index}>{website}</li>)
        ) : (
          <li className="p-4 text-gray-500">No trending websites available.</li>
        )}
      </ul>
    </div>
  );
};

export default Trending;
