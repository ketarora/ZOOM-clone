'use client';
export default function Recordings() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Recordings</h1>
      <div className="bg-surface border border-border rounded-xl overflow-hidden shadow-sm">
        <div className="flex border-b border-border bg-surface-low">
          <button className="px-6 py-3 border-b-2 border-primary text-primary font-semibold text-sm bg-surface">Cloud Recordings</button>
          <button className="px-6 py-3 border-b-2 border-transparent text-text-secondary hover:text-text-primary font-semibold text-sm">Local Recordings</button>
        </div>

        {/* Table View */}
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-low border-b border-border text-text-secondary font-semibold">
            <tr>
              <th className="p-4">Topic</th>
              <th className="p-4">ID</th>
              <th className="p-4">Start Time</th>
              <th className="p-4">File Size</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            <tr className="hover:bg-surface-low transition">
              <td className="p-4 font-medium text-primary cursor-pointer hover:underline">Weekly Sync</td>
              <td className="p-4 text-text-secondary">123-456-7890</td>
              <td className="p-4 text-text-secondary">Oct 24, 2023, 10:00 AM</td>
              <td className="p-4 text-text-secondary">156 MB</td>
            </tr>
            <tr className="hover:bg-surface-low transition">
              <td className="p-4 font-medium text-primary cursor-pointer hover:underline">Product Review</td>
              <td className="p-4 text-text-secondary">098-765-4321</td>
              <td className="p-4 text-text-secondary">Oct 23, 2023, 02:00 PM</td>
              <td className="p-4 text-text-secondary">420 MB</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
