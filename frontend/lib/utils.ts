import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export interface DateFormatOptions {
  locale?: string;
  timezone?: string;
  format?: Intl.DateTimeFormatOptions;
}

export const formatDate = (dateString: string, options?: DateFormatOptions) => {
  try {
    const locale = options?.locale || navigator.language || "en";

    // Default format for "Date, time in 24hr format"
    const defaultFormat: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
      timeZoneName: undefined
    };

    const formatOptions = {
      ...defaultFormat,
      ...options?.format
    };

    const date = new Date(dateString);
    return new Intl.DateTimeFormat(locale, formatOptions).format(date);
  } catch (error) {
    console.error("Date formatting error:", error);
    return dateString;
  }
};
