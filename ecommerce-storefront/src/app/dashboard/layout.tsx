import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/app-sidebar';
import { get_user_action } from '@/actions/auth';
import { notFound, redirect } from 'next/navigation';
interface Props {
  children: React.ReactNode;
}
export default async function Layout({ children }: Props) {
  const user = await get_user_action();
  if (!user) {
    redirect('/login');
  }
  if (!user.is_superuser) {
    notFound();
  }
  return (
    <SidebarProvider>
      <AppSidebar />
      <main className="container md:w-[calc(100%-var(--sidebar-width))] mx-auto">
        <SidebarTrigger className='md:hidden' />
        {children}
      </main>
    </SidebarProvider>
  );
}
