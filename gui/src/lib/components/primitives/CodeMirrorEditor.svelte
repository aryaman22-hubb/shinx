<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { EditorView } from '@codemirror/view';
	import { EditorState } from '@codemirror/state';
	import { sql } from '@codemirror/lang-sql';
	import { basicSetup } from 'codemirror';
	import { sqlEditorTheme, sqlSyntaxHighlighting } from './codeMirrorTheme';
	import type { CodeMirrorEditorProps } from './types/CodeMirrorEditor';

	let { value, onValueChange, readonly = false, placeholder = '', class: className = '', height = '100%', minHeight = '200px' }: CodeMirrorEditorProps = $props();

	let editorContainer: HTMLDivElement;
	let editorView: EditorView;

	onMount(() => {
		const extensions = [
			basicSetup,
			sql(),
			sqlEditorTheme,
			sqlSyntaxHighlighting,
			EditorView.updateListener.of((update) => {
				if (update.docChanged && onValueChange) {
					onValueChange(update.state.doc.toString());
				}
			}),
		];

		if (readonly) {
			extensions.push(EditorState.readOnly.of(true));
		}

		const state = EditorState.create({
			doc: value,
			extensions,
		});

		editorView = new EditorView({
			state,
			parent: editorContainer,
		});
	});

	onDestroy(() => {
		if (editorView) {
			editorView.destroy();
		}
	});

	// Update editor value when prop changes
	$effect(() => {
		if (editorView && editorView.state.doc.toString() !== value) {
			editorView.dispatch({
				changes: {
					from: 0,
					to: editorView.state.doc.length,
					insert: value,
				},
			});
		}
	});
</script>

<div bind:this={editorContainer} class={className}></div>
