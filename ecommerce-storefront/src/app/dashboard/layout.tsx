import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/app-sidebar';
import { get_super_user_action } from '@/actions/auth';
interface Props {
  children: React.ReactNode;
}
export default async function Layout({ children }: Props) {
  await get_super_user_action();

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
