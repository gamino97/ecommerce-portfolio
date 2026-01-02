import Link from 'next/link';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  ShoppingBag,
  Server,
  Shield,
  Zap,
  Database,
  Globe,
  ArrowRight,
  Code2,
  Cpu,
  Layout
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col font-sans selection:bg-primary/20">
      {/* Navigation */}
      <header className="border-b border-border/40 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-primary/10 flex items-center justify-center">
              <ShoppingBag className="w-5 h-5 text-primary" />
            </div>
            <span className="font-bold text-xl tracking-tight">NexStore</span>
          </div>
          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-muted-foreground">
            <Link href="#features" className="hover:text-foreground transition-colors">Features</Link>
            <Link href="#stack" className="hover:text-foreground transition-colors">Tech Stack</Link>
            <Link href={process.env.SOURCE_GITHUB as string} target="_blank" className="hover:text-foreground transition-colors">GitHub</Link>
          </nav>
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" asChild>
              <Link href="/login">Login</Link>
            </Button>
            <Button size="sm" asChild>
              <Link href="/store">Browse Store</Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="pt-20 pb-32 md:pt-32 md:pb-48">
          <div className="container mx-auto px-4 text-center">
            <div className="inline-flex items-center rounded-full border px-3 py-1 text-sm text-muted-foreground mb-8 bg-background/50 backdrop-blur-sm">
              <span className="h-2 w-2 rounded-full bg-primary mr-2 animate-pulse"></span>
              Full Stack E-commerce Portfolio
            </div>
            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6
              bg-gradient-to-r from-foreground to-foreground/60 bg-clip-text
              text-transparent">
              Modern E-commerce <br /> Architecture
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto mb-10 leading-relaxed">
              A high-performance storefront built with Next.js 16, FastAPI,
              and PostgreSQL. Designed for speed, scalability,
              and developer experience.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button size="lg" className="min-w-[160px] h-12 text-base" asChild>
                <Link href="/store">
                  Explore Demo <ArrowRight className="w-4 h-4" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" className="min-w-[160px] h-12 text-base" asChild>
                <Link href={process.env.SOURCE_GITHUB as string} target="_blank">
                  View Source
                </Link>
              </Button>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 bg-muted/30 border-y border-border/50">
          <div className="container mx-auto px-4">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <h2 className="text-3xl font-bold tracking-tight mb-4">Engineered for Excellence</h2>
              <p className="text-muted-foreground text-lg">
                Leveraging the latest technologies to deliver a seamless
                shopping experience and robust backend management.
              </p>
            </div>
            <div className="grid md:grid-cols-3 gap-8">
              <FeatureCard
                icon={<Zap className="w-6 h-6 text-amber-500" />}
                title="Lightning Fast"
                description="Server-side rendering with Next.js 15 App Router ensures optimal performance and SEO."
              />
              <FeatureCard
                icon={<Server className="w-6 h-6 text-blue-500" />}
                title="Python Backend"
                description="Robust API built with FastAPI, utilizing Pydantic for validation and SQLAlchemy for ORM."
              />
              <FeatureCard
                icon={<Shield className="w-6 h-6 text-green-500" />}
                title="Secure Auth"
                description="JWT-based authentication flow with secure session management and role-based access."
              />
              <FeatureCard
                icon={<Database className="w-6 h-6 text-purple-500" />}
                title="PostgreSQL"
                description="Reliable data storage using PostgreSQL, managed via Alembic migrations."
              />
              <FeatureCard
                icon={<Globe className="w-6 h-6 text-cyan-500" />}
                title="Responsive Design"
                description="Beautiful, mobile-first UI components built with Tailwind CSS and Radix UI."
              />
              <FeatureCard
                icon={<Code2 className="w-6 h-6 text-pink-500" />}
                title="Modern Standards"
                description="Written in TypeScript and Python 3.12+ with strict typing and modern patterns."
              />
            </div>
          </div>
        </section>

        {/* Tech Stack Preview */}
        <section id="stack" className="py-24">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-2xl font-bold mb-12 text-muted-foreground">Powered By</h2>
            <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-70">
              <div className="flex flex-col items-center gap-2">
                <Cpu className="w-10 h-10" />
                <span className="font-semibold">Next.js 16</span>
              </div>
              <div className="flex flex-col items-center gap-2">
                <Server className="w-10 h-10" />
                <span className="font-semibold">FastAPI</span>
              </div>
              <div className="flex flex-col items-center gap-2">
                <Layout className="w-10 h-10" />
                <span className="font-semibold">Tailwind</span>
              </div>
              <div className="flex flex-col items-center gap-2">
                <Database className="w-10 h-10" />
                <span className="font-semibold">PostgreSQL</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="py-8 border-t border-border/40 bg-muted/10">
        <div className="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-muted-foreground">
            {new Date().getFullYear()} Ecommerce Portfolio. Built by
            Carlos Gamino.
          </p>
          <div className="flex items-center gap-6 text-sm text-muted-foreground">
            <Link href={process.env.PERSONAL_WEBSITE as string} className="hover:text-foreground">About Me</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description
}: {
  icon: React.ReactNode;
  title: string;
  description: string
}) {
  return (
    <Card className="bg-card/50 border-border/50 hover:bg-card transition-colors hover:border-border">
      <CardHeader>
        <div className="h-12 w-12 rounded-lg bg-background border border-border/50 flex items-center justify-center mb-4 shadow-sm">
          {icon}
        </div>
        <CardTitle className="text-xl">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <CardDescription className="text-base leading-relaxed">
          {description}
        </CardDescription>
      </CardContent>
    </Card>
  );
}
