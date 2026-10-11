# GUI Development Guidelines for Agents

This document outlines the guidelines and best practices for making changes to the Shinx GUI.

## Data Management

### Separation of Data and UI
- Never embed data directly in UI components
- Create state variables in parent components or routes
- Pass data to UI components via props
- Keep UI components pure and data-driven

**Correct approach:**
```svelte
<!-- Route or parent component -->
<script lang="ts">
  let items = $state([
    { id: 1, name: 'Item 1' },
    { id: 2, name: 'Item 2' }
  ]);
</script>

<MyComponent {items} />
```

**Incorrect approach:**
```svelte
<!-- UI component with embedded data -->
<script lang="ts">
  let items = [
    { id: 1, name: 'Item 1' },
    { id: 2, name: 'Item 2' }
  ];
</script>

<div>
  {#each items as item}
    <div>{item.name}</div>
  {/each}
</div>
```

### When to Create State
- Create state in the route or page component for page-level data
- Create state in the nearest common ancestor for shared data
- Use props to pass data down to child components
- Use events/callbacks to communicate data changes back up

### Data Fetching
- Fetch data in route or page components
- Pass fetched data to UI components as props
- UI components should be stateless or have minimal UI-only state (e.g., open/close, selected index)

## Component Architecture

### Primitives (`gui/src/lib/components/primitives/`)
Primitives are low-level, reusable UI components that provide basic functionality and styling. These should be used as building blocks for more complex UI components.

**Available Primitives:**
- `Button` - Buttons with various variants (primary, secondary, ghost, icon, icon-bordered)
- `Input` - Text input fields with optional left/right icons
- `Picker` - Dropdown/picker component for selecting from options
- `MenuItem` - Menu item component
- `Sidebar` - Base sidebar component with slot support
- `ScreenPage` - Page layout wrapper
- `Typography` - Text styling components (h1, h2, h3, p, etc.)

**When to use primitives:**
- Always prefer using existing primitives over creating new ones
- If a primitive doesn't exist, create it in the primitives folder
- Primitives should be generic and reusable across the application
- Do not add business logic to primitives

### UI Components (`gui/src/lib/components/ui/`)
UI components are higher-level components that combine primitives and business logic to create specific features.

**Examples:**
- `DatabaseNode` - Displays a database table/view node in the visualizer
- `DatabaseVisualizer` - Main database schema visualization component
- `MainSidebar` - Application navigation sidebar
- `TableView` - Table data display component
- `TableViewSidebar` - Collapsible sidebar for table details

**When to create UI components:**
- When you need to combine multiple primitives
- When the component has business logic
- When the component is specific to a feature (e.g., database visualization)
- Keep UI components focused on a single responsibility

## Type Organization

### Type Files
All TypeScript interfaces and types must be extracted to dedicated type files in the `types/` folder within each component directory.

**Structure:**
```
components/
  ui/
    MyComponent.svelte
    types/
      MyComponent.ts  <-- Types live here
  primitives/
    MyPrimitive.svelte
    types/
      MyPrimitive.ts  <-- Types live here
```

**Rules:**
- Never define interfaces/types inline in `.svelte` files
- Export all types from the corresponding `.ts` file
- Import types using relative paths: `import type { MyComponentProps } from './types/MyComponent'`
- Name the type file after the component it belongs to

## Composition Over Monolith

### Prefer Composition
- Build complex UIs by composing smaller, focused components
- Use slots/snippets for flexible content composition
- Keep components shallow - avoid deeply nested component hierarchies

### Avoid Monoliths
- Do not create massive components that handle multiple concerns
- Split large components into smaller, reusable pieces
- If a component is doing too much, extract sub-components

## Svelte 5 Specific Guidelines

### Runes Mode
- Use `$state` for reactive state
- Use `$derived` for computed values
- Use `$props` for component props
- Use `$bindable` for two-way bindings

### Snippets over Component Props
- When passing dynamic content (icons, etc.), use snippets instead of component props
- Correct:
  ```svelte
  <Input>
    {#snippet leftIcon()}
      <Search size={18} />
    {/snippet}
  </Input>
  ```
- Incorrect (deprecated in runes mode):
  ```svelte
  <Input leftIcon={Search} />
  ```

### Avoid `<svelte:component>`
- Components are dynamic by default in runes mode
- Use direct component rendering or snippets instead

## Styling Guidelines

### Tailwind Variants
- Use `tailwind-variants` (tv) for component styling
- Define variants in the component script
- Keep base styles, variants, and default variants organized

### Color Palette
Use the defined color palette from `app.css`:
- `--color-primary: #7ecdf3`
- `--color-secondary: #161212`
- `--color-highlight: #f9bf00`
- `--color-on-surface: #eae0df`
- `--color-on-surface-variant: #bfc8ce`
- `--color-outline: #899298`

### Typography
- Use the `Typography` primitive for all text
- Use the defined font family: `Poppins`

## File Naming Conventions

- Component files: `PascalCase.svelte`
- Type files: `PascalCase.ts`
- Folders: `kebab-case` or `PascalCase` (match component name)

## Before Making Changes

1. **Check existing primitives** - Look in `components/primitives/` for reusable components
2. **Check existing UI components** - Look in `components/ui/` for similar patterns
3. **Extract types** - Create a type file if you're adding new interfaces
4. **Follow composition** - Break down complex features into smaller components
5. **Use snippets** - For dynamic content, use Svelte 5 snippet syntax

## Example Workflow

**Adding a new feature:**

1. Identify if you need a new primitive or UI component
2. Create the component file
3. Create the types file in the `types/` folder
4. Implement the component using existing primitives
5. Use slots/snippets for flexible content
6. Add the component to the appropriate route
7. Test the component

**Example:**
```svelte
<!-- ui/types/MyFeature.ts -->
export interface MyFeatureProps {
  data: Data;
  onAction?: () => void;
}

<!-- ui/MyFeature.svelte -->
<script lang="ts">
  import Button from '#lib/components/primitives/Button.svelte';
  import Input from '#lib/components/primitives/Input.svelte';
  import type { MyFeatureProps } from './types/MyFeature';

  let { data, onAction }: MyFeatureProps = $props();
</script>

<div class="flex gap-2">
  <Input placeholder="Search" />
  <Button onclick={onAction}>Action</Button>
</div>
```

## Performance Considerations

- Use `$state.raw` for large arrays/objects that don't need deep reactivity (e.g., flow nodes)
- Avoid unnecessary re-renders by using `$derived` for computed values
- Keep component trees shallow

## Testing

- Test components in isolation
- Verify type safety
- Ensure proper error handling

## Summary

- ✅ Use primitives for basic UI elements
- ✅ Create UI components for feature-specific logic
- ✅ Extract types to dedicated `types/` folders
- ✅ Prefer composition over monolithic components
- ✅ Use Svelte 5 runes and snippets
- ✅ Follow established patterns and conventions
- ❌ Don't define types inline
- ❌ Don't create monolithic components
- ❌ Don't use deprecated `<svelte:component>` in runes mode
