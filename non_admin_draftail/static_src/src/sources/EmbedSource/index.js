import React, {Component} from "react";

import {AtomicBlockUtils} from "draft-js";

import Modal from "../../components/Modal/Modal";
import "./Style.scss";

export class EmbedSource extends Component {
  constructor(props) {
    super(props);
    const {entity} = this.props;
    const state = {
      url: "",
      validationError: null
    };

    if (entity) {
      const data = entity.getData();
      state.url = data.url;
    }

    this.state = state;

    this.onRequestClose = this.onRequestClose.bind(this);
    this.onAfterOpen = this.onAfterOpen.bind(this);
    this.onConfirm = this.onConfirm.bind(this);
    this.onBlurURL = this.onBlurURL.bind(this);
    this.onChangeURL = this.onChangeURL.bind(this);
    this.validateUrl = this.validateUrl.bind(this);
  }

  /* :: onConfirm: (e: Event) => void; */
  async onConfirm(e) {
    const {editorState, entityType, onComplete} = this.props;
    const {url} = this.state;
    e.preventDefault();

    if (!this.validateUrl(url)) {
      return;
    }

    try {
      const res = await fetch(window.nonAdminDraftailConfig.URLS.embed_upload, {
        method: 'POST',
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({
          url
        }),
      })

      if (res.status === 400) {
        const errorText = await res.text();
        this.setState(({validationError: errorText}));
        return;
      }

      const data = await res.json();
      const entityData = {
        embedType: data.embedType,
        url: data.url,
        providerName: data.providerName,
        authorName: data.authorName,
        thumbnail: data.thumbnail,
        title: data.title,
      };

      const content = editorState.getCurrentContent();
      const contentWithEntity = content.createEntity(entityType.type, 'IMMUTABLE', entityData);
      const entityKey = contentWithEntity.getLastCreatedEntityKey();
      const nextState = AtomicBlockUtils.insertAtomicBlock(editorState, entityKey, ' ');
      onComplete(nextState);
    } catch (e) {
      console.error(e);
      this.setState(({validationError: "Something went wrong. Please try again."}));
    }
  }

  /* :: onRequestClose: (e: SyntheticEvent<>) => void; */
  onRequestClose(e) {
    const {onClose} = this.props;
    e.preventDefault();

    onClose();
  }

  /* :: onAfterOpen: () => void; */
  onAfterOpen() {
    const input = this.inputRef;

    if (input) {
      input.focus();
      input.select();
    }
  }

  onBlurURL(e) {
    const url = e.target.value;
    this.validateUrl(url);
  }

  /* :: onChangeURL: (e: Event) => void; */
  onChangeURL(e) {
    const url = e.target.value;
    this.setState({url, validationError: null});
  }

  validateUrl(url) {
    const isValid = isValidUrl(url);
    this.setState(({validationError: !isValid ? "Please provide a valid URL" : null}));
    return isValid;
  }

  render() {
    const {url} = this.state;
    return (
      <Modal
        onRequestClose={this.onRequestClose}
        onAfterOpen={this.onAfterOpen}
        isOpen
        contentLabel="Embed chooser"
      >
        <form className="non-admin-draftail__EmbedSource" onSubmit={this.onConfirm}>
          <div className="non-admin-draftail__EmbedSource__field">
            <label htmlFor="url">Media embed URL</label>
            <input
              ref={(inputRef) => {
                this.inputRef = inputRef;
              }}
              name="url"
              type="text"
              onChange={this.onChangeURL}
              onBlur={this.onBlurURL}
              value={url}
            />
            {this.state.validationError && <p className="non-admin-draftail__EmbedSource__validationError">
              {this.state.validationError}
            </p>}
          </div>
          <button disabled={this.state.validationError} type="submit">Insert</button>
        </form>
      </Modal>
    );
  }
}

const isValidUrl = url => {
  const validUrlPattern = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/;
  return validUrlPattern.test(url.toLowerCase());
};

const getCookie = name => ('; ' + document.cookie).split('; ' + name + '=').pop().split(';').shift();