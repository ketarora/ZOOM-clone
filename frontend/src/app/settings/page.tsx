'use client';
export default function Settings() {
  return (
    <div className="flex h-[calc(100vh-var(--topbar-h))]">
      {/* Left side nav (Settings specific) */}
      <div className="w-64 border-r border-border bg-surface flex flex-col p-4">
        <h2 className="text-xl font-bold mb-4 px-2">Settings</h2>
        <nav className="space-y-1">
          <a className="block px-3 py-2 rounded-lg bg-primary-light text-primary font-medium" href="#">Profile</a>
          <a className="block px-3 py-2 rounded-lg text-text-secondary hover:bg-surface-low hover:text-text-primary transition-colors" href="#">Meeting</a>
          <a className="block px-3 py-2 rounded-lg text-text-secondary hover:bg-surface-low hover:text-text-primary transition-colors" href="#">Recording</a>
          <a className="block px-3 py-2 rounded-lg text-text-secondary hover:bg-surface-low hover:text-text-primary transition-colors" href="#">Audio Conferencing</a>
          <a className="block px-3 py-2 rounded-lg text-text-secondary hover:bg-surface-low hover:text-text-primary transition-colors" href="#">Collaboration Devices</a>
        </nav>
      </div>

      {/* Main content */}
      <div className="flex-1 p-8 overflow-y-auto">
        <div className="max-w-3xl">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-24 h-24 rounded-full bg-primary-light flex items-center justify-center text-4xl font-bold text-primary">A</div>
            <div>
              <h1 className="text-3xl font-bold text-text-primary">Alex Thompson</h1>
              <p className="text-text-secondary mt-1">alex@zoomconnect.demo</p>
              <button className="text-primary text-sm font-medium hover:underline mt-2">Edit</button>
            </div>
          </div>

          <div className="space-y-8">
            <section className="bg-surface border border-border rounded-xl p-6">
              <h3 className="text-lg font-semibold text-text-primary mb-4 border-b border-border pb-2">Personal Information</h3>
              <div className="space-y-4">
                <div className="flex">
                  <div className="w-1/3 text-sm text-text-secondary font-medium">Department</div>
                  <div className="w-2/3 text-sm text-text-primary">Engineering</div>
                </div>
                <div className="flex">
                  <div className="w-1/3 text-sm text-text-secondary font-medium">Job Title</div>
                  <div className="w-2/3 text-sm text-text-primary">Senior Software Engineer</div>
                </div>
                <div className="flex">
                  <div className="w-1/3 text-sm text-text-secondary font-medium">Company</div>
                  <div className="w-2/3 text-sm text-text-primary">ZoomConnect Inc.</div>
                </div>
              </div>
            </section>

            <section className="bg-surface border border-border rounded-xl p-6">
              <h3 className="text-lg font-semibold text-text-primary mb-4 border-b border-border pb-2">Meeting Details</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-text-primary">Personal Meeting ID</div>
                    <div className="text-sm text-text-secondary mt-1">123-456-7890</div>
                  </div>
                  <button className="btn-secondary text-sm py-1.5 px-3">Edit</button>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-text-primary">Personal Link</div>
                    <div className="text-sm text-text-secondary mt-1">https://zoomconnect.demo/my/alex</div>
                  </div>
                  <button className="btn-secondary text-sm py-1.5 px-3">Customize</button>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}
