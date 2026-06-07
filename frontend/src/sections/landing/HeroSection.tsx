import { Button } from "@/components/ui/button";
import { ArrowRight, Graph, Lightbulb, RocketLaunch } from "@phosphor-icons/react";
import { Link } from "react-router-dom";

export function HeroSection() {
  return (
    <section className="relative w-full min-h-screen flex items-center justify-center overflow-hidden bg-background">
      {/* Background gradients */}
      <div className="absolute inset-0 z-0">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] rounded-full bg-primary/20 blur-[120px] pointer-events-none" />
        <div className="absolute top-[20%] -right-[10%] w-[30%] h-[50%] rounded-full bg-accent/20 blur-[120px] pointer-events-none" />
      </div>

      <div className="container relative z-10 mx-auto px-4 md:px-6 flex flex-col items-center text-center">
        <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80 mb-6">
          <RocketLaunch weight="fill" className="mr-2 h-4 w-4 text-primary" />
          <span>OculusLab Grafos V2.0</span>
        </div>
        
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-foreground max-w-4xl mb-6">
          Visualiza la Complejidad de los <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">Grafos</span>
        </h1>
        
        <p className="text-muted-foreground text-lg md:text-xl max-w-2xl mb-10 leading-relaxed">
          Una plataforma avanzada diseñada para la experimentación, análisis y comprensión de estructuras de datos complejas. Explora algoritmos en tiempo real.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <Link to="/explorer">
            <Button size="lg" className="rounded-full px-8 text-base h-12 shadow-lg hover:shadow-primary/25 transition-all w-full sm:w-auto">
              Empezar Laboratorio
              <ArrowRight weight="bold" className="ml-2 h-5 w-5" />
            </Button>
          </Link>
          <Button size="lg" variant="outline" className="rounded-full px-8 text-base h-12 bg-background/50 backdrop-blur-sm w-full sm:w-auto">
            <Graph weight="duotone" className="mr-2 h-5 w-5" />
            Ver Documentación
          </Button>
        </div>

        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl text-left border-t border-border/50 pt-10">
          <div className="flex flex-col items-start gap-2">
            <div className="p-3 rounded-lg bg-primary/10 text-primary mb-2 shadow-inner">
              <Graph weight="duotone" className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold">Análisis Profundo</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Descubre patrones ocultos y métricas clave en cualquier estructura de red o grafo dirigido.
            </p>
          </div>
          <div className="flex flex-col items-start gap-2">
            <div className="p-3 rounded-lg bg-accent/10 text-accent mb-2 shadow-inner">
              <Lightbulb weight="duotone" className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold">Algoritmos Visuales</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Aprende interactivamente viendo cómo Dijkstra, DFS y BFS resuelven problemas paso a paso.
            </p>
          </div>
          <div className="flex flex-col items-start gap-2">
            <div className="p-3 rounded-lg bg-primary/10 text-primary mb-2 shadow-inner">
              <RocketLaunch weight="duotone" className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold">Rendimiento Extremo</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Maneja grafos densos de miles de nodos gracias a la optimización de renderizado.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
