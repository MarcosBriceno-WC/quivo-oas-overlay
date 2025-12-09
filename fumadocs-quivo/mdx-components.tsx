import defaultMdxComponents from "fumadocs-ui/mdx";
import type { MDXComponents } from "mdx/types";
import React from "react";
import {
  Warehouse,
  ShoppingCart,
  MapPin,
  RotateCcw,
  Bell,
  HelpCircle,
  Rocket,
  Book,
  Key,
} from "lucide-react";
import * as TabsPrimitive from "@radix-ui/react-tabs";
import { APIPage } from "@/components/api-page";

// Get Card and Cards from default components if available
const FumadocsCard = (defaultMdxComponents as any).Card;
const FumadocsCards = (defaultMdxComponents as any).Cards;

// Simple cn utility function
function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(" ");
}

// Icon map for string-based icon names
const iconMap: Record<string, React.ReactNode> = {
  warehouse: <Warehouse className="w-5 h-5" />,
  "shopping-cart": <ShoppingCart className="w-5 h-5" />,
  "location-dot": <MapPin className="w-5 h-5" />,
  "rotate-left": <RotateCcw className="w-5 h-5" />,
  bell: <Bell className="w-5 h-5" />,
  "question-circle": <HelpCircle className="w-5 h-5" />,
  rocket: <Rocket className="w-5 h-5" />,
  book: <Book className="w-5 h-5" />,
  key: <Key className="w-5 h-5" />,
};

// Card component wrapper that converts string icons to React elements
function Card({
  title,
  icon,
  href,
  children,
  ...props
}: {
  title: string;
  icon?: string | React.ReactNode;
  href?: string;
  children: React.ReactNode;
}) {
  // Convert string icon to React element if needed
  const iconElement = typeof icon === "string" ? iconMap[icon] : icon;

  // Use fumadocs Card if available
  if (FumadocsCard) {
    return (
      <FumadocsCard title={title} icon={iconElement} href={href} {...props}>
        {children}
      </FumadocsCard>
    );
  }

  // Fallback: custom implementation matching fumadocs style
  return (
    <a
      href={href}
      className="group flex flex-col gap-2 rounded-lg border border-border bg-card p-4 transition-all hover:border-primary/50 hover:bg-accent/50 hover:shadow-sm"
    >
      {iconElement && (
        <div className="text-muted-foreground transition-colors group-hover:text-foreground">
          {iconElement}
        </div>
      )}
      <h3 className="font-semibold text-base leading-tight">{title}</h3>
      <p className="text-sm leading-relaxed text-muted-foreground">
        {children}
      </p>
    </a>
  );
}

// Cards component wrapper - use fumadocs Cards if available
function Cards({ children, ...props }: { children: React.ReactNode }) {
  if (FumadocsCards) {
    return <FumadocsCards {...props}>{children}</FumadocsCards>;
  }
  // Fallback: simple grid layout matching fumadocs style
  return (
    <div className="my-4 grid gap-3 grid-cols-1 md:grid-cols-2">{children}</div>
  );
}

// CardGroup component (alias for Cards for compatibility)
function CardGroup({
  cols,
  children,
  ...props
}: {
  cols?: number;
  children: React.ReactNode;
}) {
  return <Cards {...props}>{children}</Cards>;
}

// Mintlify-style callout components - using fumadocs Callout if available, otherwise custom styling
function Note({ children }: { children: React.ReactNode }) {
  const Callout = (defaultMdxComponents as any).Callout;
  if (Callout) {
    return <Callout type="info">{children}</Callout>;
  }
  return (
    <div className="my-4 rounded-lg border border-blue-200 bg-blue-50 p-4 dark:border-blue-800 dark:bg-blue-950">
      <p className="text-sm">{children}</p>
    </div>
  );
}

function Tip({ children }: { children: React.ReactNode }) {
  const Callout = (defaultMdxComponents as any).Callout;
  if (Callout) {
    return <Callout type="tip">{children}</Callout>;
  }
  return (
    <div className="my-4 rounded-lg border border-green-200 bg-green-50 p-4 dark:border-green-800 dark:bg-green-950">
      <p className="text-sm">{children}</p>
    </div>
  );
}

function Warning({ children }: { children: React.ReactNode }) {
  const Callout = (defaultMdxComponents as any).Callout;
  if (Callout) {
    return <Callout type="warn">{children}</Callout>;
  }
  return (
    <div className="my-4 rounded-lg border border-yellow-200 bg-yellow-50 p-4 dark:border-yellow-800 dark:bg-yellow-950">
      <p className="text-sm">{children}</p>
    </div>
  );
}

function Info({ children }: { children: React.ReactNode }) {
  const Callout = (defaultMdxComponents as any).Callout;
  if (Callout) {
    return <Callout type="info">{children}</Callout>;
  }
  return (
    <div className="my-4 rounded-lg border border-blue-200 bg-blue-50 p-4 dark:border-blue-800 dark:bg-blue-950">
      <p className="text-sm">{children}</p>
    </div>
  );
}

function Check({ children }: { children: React.ReactNode }) {
  const Callout = (defaultMdxComponents as any).Callout;
  if (Callout) {
    return <Callout type="check">{children}</Callout>;
  }
  return (
    <div className="my-4 rounded-lg border border-green-200 bg-green-50 p-4 dark:border-green-800 dark:bg-green-950">
      <p className="text-sm">{children}</p>
    </div>
  );
}

function CalloutComponent({ children }: { children: React.ReactNode }) {
  const Callout = (defaultMdxComponents as any).Callout;
  if (Callout) {
    return <Callout>{children}</Callout>;
  }
  return (
    <div className="my-4 rounded-lg border border-border bg-card p-4">
      <p className="text-sm">{children}</p>
    </div>
  );
}

// Tabs component for fumadocs
function Tabs({
  children,
  defaultValue,
}: {
  children: React.ReactNode;
  defaultValue?: string;
}) {
  const tabs = React.Children.toArray(children) as React.ReactElement<{
    title?: string;
    value?: string;
    children?: React.ReactNode;
  }>[];
  const firstTab = tabs.find((tab) => {
    const props = tab.props as { title?: string; value?: string };
    return props.title || props.value;
  });
  const firstValue =
    (firstTab?.props as { title?: string; value?: string })?.title ||
    (firstTab?.props as { title?: string; value?: string })?.value ||
    defaultValue ||
    "tab-0";

  return (
    <TabsPrimitive.Root defaultValue={firstValue} className="my-4">
      <TabsPrimitive.List className="inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground">
        {tabs.map((tab, index) => {
          const props = tab.props as {
            title?: string;
            value?: string;
            children?: React.ReactNode;
          };
          const title = props.title || props.value || `Tab ${index + 1}`;
          const value = props.value || props.title || `tab-${index}`;
          return (
            <TabsPrimitive.Trigger
              key={value}
              value={value}
              className={cn(
                "inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm"
              )}
            >
              {title}
            </TabsPrimitive.Trigger>
          );
        })}
      </TabsPrimitive.List>
      {tabs.map((tab, index) => {
        const props = tab.props as {
          title?: string;
          value?: string;
          children?: React.ReactNode;
        };
        const value = props.value || props.title || `tab-${index}`;
        return (
          <TabsPrimitive.Content
            key={value}
            value={value}
            className="mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            {props.children}
          </TabsPrimitive.Content>
        );
      })}
    </TabsPrimitive.Root>
  );
}

// Tab component - used as a child of Tabs
function Tab({
  title,
  value,
  children,
}: {
  title?: string;
  value?: string;
  children: React.ReactNode;
}) {
  return <>{children}</>;
}

export function getMDXComponents(components?: MDXComponents): MDXComponents {
  return {
    ...defaultMdxComponents,
    // Custom components
    Card,
    CardGroup,
    Cards,
    Note,
    Tip,
    Warning,
    Info,
    Check,
    Callout: CalloutComponent,
    Tabs,
    Tab,
    APIPage,
    ...components,
  };
}
