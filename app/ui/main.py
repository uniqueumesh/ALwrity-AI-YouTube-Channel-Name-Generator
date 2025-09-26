import streamlit as st

# Ensure absolute imports like `from app...` work even when running this nested file directly.
try:  # type: ignore
    from app.core.prompt import build_generation_request
    from app.services.gemini import generate_names
    from app.utils.session import get_session_state
except ModuleNotFoundError:  # pragma: no cover
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from app.core.prompt import build_generation_request
    from app.services.gemini import generate_names
    from app.utils.session import get_session_state


def render_main_page() -> None:
    st.set_page_config(page_title="ALwrity AI YouTube Channel Name Generator", page_icon="🎬", layout="centered")

    state = get_session_state()

    st.title("ALwrity AI YouTube Channel Name Generator")
    

    with st.container():
        description = st.text_area(
            "Channel short description*",
            placeholder="e.g., Tutorials for beginners on Python and data science",
            value=state.get("description", ""),
        )

        languages = [
            "English",
            "Hindi",
            "French",
            "Spanish",
            "German",
            "Arabic",
            "Portuguese",
            "Bengali",
            "Japanese",
            "Korean",
            "Custom",
        ]
        language_choice = st.selectbox("Language*", options=languages, index=0)
        custom_language = ""
        if language_choice == "Custom":
            custom_language = st.text_input("Custom language*", placeholder="e.g., Gujarati")

        variants = st.selectbox("Variants*", options=[5, 10, 15, 20], index=1)
        explain = st.checkbox("Explain the meaning of generated names", value=False)

        tones = ["Friendly", "Professional", "Casual", "Educational", "Playful", "Bold", "Custom"]
        tone_choice = st.selectbox("Tone*", options=tones, index=0)
        custom_tone = ""
        if tone_choice == "Custom":
            custom_tone = st.text_input("Custom tone*", placeholder="e.g., inspirational")

        api_key = st.text_input("Gemini API Key*", type="password", placeholder="Paste your Gemini API key")

        generate_clicked = st.button("Generate Name Ideas", type="primary")

    if generate_clicked:
        # Validate inputs
        if not description.strip():
            st.error("Please enter a channel short description.")
            return
        if language_choice == "Custom" and not custom_language.strip():
            st.error("Please enter a custom language.")
            return
        if tone_choice == "Custom" and not custom_tone.strip():
            st.error("Please enter a custom tone.")
            return
        if not api_key.strip():
            st.error("Please enter your Gemini API key.")
            return

        # Persist minimal state
        state["description"] = description

        target_language = custom_language.strip() if language_choice == "Custom" else language_choice
        tone = custom_tone.strip() if tone_choice == "Custom" else tone_choice

        request_payload = build_generation_request(
            description=description.strip(),
            language=target_language,
            variants=int(variants),
            tone=tone,
            explain_meanings=bool(explain),
        )

        with st.spinner("Generating ideas..."):
            try:
                result = generate_names(api_key=api_key.strip(), request=request_payload)
            except Exception as exc:
                st.error(f"Generation failed: {exc}")
                return

        ideas = result.get("ideas", [])
        explanations = result.get("explanations", []) if explain else []

        # Post-filter for sentences/long phrases
        try:
            from app.core.prompt import sanitize_ideas
            ideas = sanitize_ideas(ideas)
        except Exception:
            pass

        if not ideas:
            st.warning("No ideas were returned. Try adjusting your inputs and generate again.")
            return

        # Persist results in session so UI doesn't reset on reruns
        state["ideas"] = ideas
        state["explanations"] = explanations

    # Render results if present in session (prevents reset on reruns)
    session_ideas: list[str] = state.get("ideas", [])
    session_explanations: list[str] = state.get("explanations", [])
    if session_ideas:
        st.subheader("Results")
        shortlist = state.setdefault("shortlist", [])

        for idx, idea in enumerate(session_ideas):
            with st.container(border=True):
                st.markdown(f"**{idea}**")
                if idx < len(session_explanations) and session_explanations[idx]:
                    st.caption(session_explanations[idx])
                cols = st.columns(3)
                with cols[0]:
                    st.button("Copy name", key=f"copy_name_{idx}", on_click=lambda n=idea: st.session_state.update({"clipboard": n}))
                with cols[1]:
                    both = f"{idea} — {session_explanations[idx]}" if idx < len(session_explanations) and session_explanations[idx] else idea
                    st.button("Copy name + explanation", key=f"copy_both_{idx}", on_click=lambda b=both: st.session_state.update({"clipboard": b}))
                with cols[2]:
                    def add_to_shortlist(name: str, meaning: str | None) -> None:
                        shortlist.append({"name": name, "meaning": meaning})

                    st.button(
                        "Add to shortlist",
                        key=f"shortlist_{idx}",
                        on_click=add_to_shortlist,
                        args=(idea, session_explanations[idx] if idx < len(session_explanations) and session_explanations[idx] else None),
                    )

        st.divider()
        st.subheader("Shortlist")
        if not shortlist:
            st.caption("Your shortlisted names will appear here.")
        else:
            for item in shortlist:
                st.write(item["name"]) if not item.get("meaning") else st.write(f"{item['name']} — {item['meaning']}")

        # Optional Logo Section (does not affect core generation)
        try:
            from app.ui.logo import render_logo_section
            available_names = list(session_ideas) + [i["name"] for i in shortlist if isinstance(i, dict) and i.get("name")]
            # De-duplicate while preserving order
            seen = set()
            unique_names: list[str] = []
            for n in available_names:
                if n not in seen:
                    seen.add(n)
                    unique_names.append(n)
            render_logo_section(unique_names)
        except Exception:
            pass


if __name__ == "__main__":
    render_main_page()


