import { Navbar } from '@/components/Navbar';
import { get_user_action } from '@/actions/auth';

export default async function StoreLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const user = await get_user_action();
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar user={user} />
      <main className="flex-1 container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="border-t border-border/40 py-6 bg-muted/10 mt-auto">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          &copy; {new Date().getFullYear()} NexStore. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
