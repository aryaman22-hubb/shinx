import { EditorView } from '@codemirror/view';
import { HighlightStyle, syntaxHighlighting } from '@codemirror/language';
import { tags } from '@lezer/highlight';

const colors = {
	background: '#231f1e',
	backgroundDark: '#1a1716',
	backgroundElevated: '#302a28',
	backgroundHover: '#3a3330',
	backgroundSelected: '#403832',

	primary: '#7ecdf3',
	primaryMuted: 'rgba(126, 205, 243, 0.15)',
	primarySelection: 'rgba(126, 205, 243, 0.30)',

	highlight: '#f9bf00',
	highlightMuted: 'rgba(249, 191, 0, 0.18)',

	text: '#eae0df',
	textMuted: '#bfc8ce',
	textSubtle: '#899298',

	green: '#a8d9a0',
	orange: '#f2a65a',
	purple: '#c5a3ff',
	red: '#ff8b8b',

	border: '#45403e',
	borderFocused: '#7ecdf3',
};

export const sqlEditorTheme = EditorView.theme(
	{
		// Editor container
		'&': {
			color: colors.text,
			backgroundColor: colors.background,
			height: '100%',
			minHeight: '200px',
			fontSize: '14px',
		},

		'&.cm-focused': {
			outline: 'none',
		},

		// Scrolling area
		'.cm-scroller': {
			overflow: 'auto',
			fontFamily:
				'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
			lineHeight: '1.7',
		},

		// Editor text
		'.cm-content': {
			padding: '16px 0',
			caretColor: colors.primary,
		},

		'.cm-line': {
			padding: '0 20px',
		},

		'.cm-cursor, .cm-dropCursor': {
			borderLeftColor: colors.primary,
			borderLeftWidth: '2px',
		},

		// Gutters and line numbers
		'.cm-gutters': {
			backgroundColor: colors.backgroundDark,
			color: colors.textSubtle,
			border: 'none',
			borderRight: `1px solid ${colors.border}`,
			paddingRight: '8px',
		},

		'.cm-lineNumbers .cm-gutterElement': {
			padding: '0 10px 0 16px',
			minWidth: '36px',
		},

		'.cm-activeLineGutter': {
			backgroundColor: colors.backgroundElevated,
			color: colors.primary,
		},

		'.cm-activeLine': {
			backgroundColor: 'rgba(126, 205, 243, 0.055)',
		},

		// Selection
		'.cm-selectionBackground': {
			backgroundColor: colors.primarySelection,
		},

		'&.cm-focused .cm-selectionBackground': {
			backgroundColor: 'rgba(126, 205, 243, 0.25)',
		},

		'.cm-selectionMatch': {
			backgroundColor: colors.highlightMuted,
			outline: `1px solid rgba(249, 191, 0, 0.25)`,
		},

		// Matching brackets
		'.cm-matchingBracket': {
			color: colors.highlight,
			backgroundColor: colors.highlightMuted,
			outline: `1px solid rgba(249, 191, 0, 0.35)`,
		},

		'.cm-nonmatchingBracket': {
			color: colors.red,
			backgroundColor: 'rgba(255, 139, 139, 0.12)',
		},

		// Autocomplete dropdown
		'.cm-tooltip': {
			backgroundColor: colors.backgroundElevated,
			color: colors.text,
			border: `1px solid ${colors.border}`,
			borderRadius: '8px',
			boxShadow: '0 12px 32px rgba(0, 0, 0, 0.35)',
			overflow: 'hidden',
		},

		'.cm-tooltip-autocomplete': {
			'& > ul': {
				fontFamily:
					'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
				maxHeight: '240px',
				padding: '4px',
			},

			'& > ul > li': {
				padding: '6px 10px',
				borderRadius: '4px',
				color: colors.textMuted,
			},

			'& > ul > li[aria-selected]': {
				backgroundColor: colors.backgroundSelected,
				color: colors.primary,
			},

			'& > ul > li[aria-selected] .cm-completionLabel': {
				color: colors.primary,
			},
		},

		'.cm-completionLabel': {
			color: colors.text,
		},

		'.cm-completionDetail': {
			color: colors.textSubtle,
			fontStyle: 'normal',
			marginLeft: '12px',
		},

		'.cm-completionMatchedText': {
			color: colors.highlight,
			textDecoration: 'none',
			fontWeight: '600',
		},

		'.cm-completionIcon': {
			opacity: '0.9',
		},

		// Autocomplete category icons
		'.cm-completionIcon-function': {
			color: colors.purple,
		},

		'.cm-completionIcon-variable': {
			color: colors.primary,
		},

		'.cm-completionIcon-keyword': {
			color: colors.highlight,
		},

		'.cm-completionIcon-class': {
			color: colors.green,
		},

		// Search panel
		'.cm-panels': {
			backgroundColor: colors.backgroundDark,
			color: colors.text,
		},

		'.cm-panels-top': {
			borderBottom: `1px solid ${colors.border}`,
		},

		'.cm-panels-bottom': {
			borderTop: `1px solid ${colors.border}`,
		},

		'.cm-search': {
			padding: '8px 12px',
			display: 'flex',
			flexWrap: 'wrap',
			gap: '8px',
			alignItems: 'center',
		},

		'.cm-search input, .cm-search button, .cm-button': {
			backgroundColor: colors.backgroundElevated,
			color: colors.text,
			border: `1px solid ${colors.border}`,
			borderRadius: '5px',
			padding: '5px 8px',
		},

		'.cm-search input:focus': {
			outline: `1px solid ${colors.primary}`,
			borderColor: colors.primary,
		},

		'.cm-search button:hover, .cm-button:hover': {
			backgroundColor: colors.backgroundHover,
		},

		'.cm-searchMatch': {
			backgroundColor: colors.highlightMuted,
			outline: `1px solid rgba(249, 191, 0, 0.35)`,
		},

		'.cm-searchMatch-selected': {
			backgroundColor: 'rgba(249, 191, 0, 0.32)',
			outline: `1px solid ${colors.highlight}`,
		},

		// Lint / diagnostic tooltips
		'.cm-diagnostic': {
			padding: '6px 10px',
		},

		'.cm-tooltip-lint': {
			backgroundColor: colors.backgroundElevated,
			border: `1px solid ${colors.border}`,
			borderRadius: '6px',
		},

		'.cm-diagnostic-error': {
			borderLeftColor: colors.red,
		},

		'.cm-diagnostic-warning': {
			borderLeftColor: colors.highlight,
		},

		// Fold controls
		'.cm-foldPlaceholder': {
			backgroundColor: colors.backgroundElevated,
			color: colors.primary,
			border: `1px solid ${colors.border}`,
			borderRadius: '4px',
			padding: '0 5px',
		},

		'.cm-foldGutter span': {
			color: colors.textSubtle,
		},

		// Read-only / disabled editor
		'&.cm-readonly .cm-content': {
			opacity: '0.75',
		},

		// Scrollbars
		'.cm-scroller::-webkit-scrollbar': {
			width: '10px',
			height: '10px',
		},

		'.cm-scroller::-webkit-scrollbar-track': {
			backgroundColor: colors.background,
		},

		'.cm-scroller::-webkit-scrollbar-thumb': {
			backgroundColor: colors.border,
			borderRadius: '8px',
			border: `2px solid ${colors.background}`,
		},

		'.cm-scroller::-webkit-scrollbar-thumb:hover': {
			backgroundColor: colors.textSubtle,
		},
	},
	{ dark: true },
);

// SQL syntax highlighting
export const sqlSyntaxHighlighting = syntaxHighlighting(
	HighlightStyle.define([
		// SQL keywords: SELECT, FROM, WHERE, JOIN, etc.
		{
			tag: tags.keyword,
			color: colors.primary,
			fontWeight: '600',
		},

		// Strings: 'hello', 'active'
		{
			tag: tags.string,
			color: colors.green,
		},

		// Numbers
		{
			tag: tags.number,
			color: colors.orange,
		},

		// Comments
		{
			tag: tags.comment,
			color: colors.textSubtle,
			fontStyle: 'italic',
		},

		// SQL operators
		{
			tag: tags.operator,
			color: colors.highlight,
		},

		// Function names
		{
			tag: tags.function(tags.variableName),
			color: colors.purple,
		},

		// Table names and column identifiers
		{
			tag: tags.variableName,
			color: colors.text,
		},

		// Properties / field names
		{
			tag: tags.propertyName,
			color: colors.primary,
		},

		// Types: INTEGER, VARCHAR, BOOLEAN
		{
			tag: tags.typeName,
			color: colors.orange,
		},

		// Boolean and null literals
		{
			tag: tags.bool,
			color: colors.highlight,
		},

		{
			tag: tags.null,
			color: colors.red,
		},

		// Punctuation: commas, semicolons, parentheses
		{
			tag: tags.punctuation,
			color: colors.textMuted,
		},

		// SQL constants
		{
			tag: tags.constant(tags.name),
			color: colors.highlight,
		},

		// Definition names
		{
			tag: tags.definition(tags.variableName),
			color: colors.primary,
		},
	]),
);
