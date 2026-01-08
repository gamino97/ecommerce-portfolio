'use client';
import { redirect } from 'next/navigation';
import { SidebarMenuButton } from '@/components/ui/sidebar';
import { LogOutIcon } from 'lucide-react';
import { logoutAction } from '@/actions/auth';

export function SignOut() {
  async function signOut() {
    await logoutAction();
    redirect('/login');
  }
  return (
    <SidebarMenuButton onClick={signOut} className='cursor-pointer'>
      <LogOutIcon />
      <span>Log out</span>
    </SidebarMenuButton>
  );
}
