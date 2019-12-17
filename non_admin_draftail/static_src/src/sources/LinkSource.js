import React, {Component} from "react";

import {RichUtils} from "draft-js";

import Modal from "../components/Modal/Modal";
import "./LinkSource.scss";

class LinkSource extends Component {
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
  onConfirm(e) {
    const {editorState, entityType, onComplete} = this.props;
    const {url} = this.state;

    e.preventDefault();

    if (!this.validateUrl(url)) {
      return;
    }

    const contentState = editorState.getCurrentContent();
    const data = {
      url: url.replace(/\s/g, ""),
    };
    const contentStateWithEntity = contentState.createEntity(
      // Fixed in https://github.com/facebook/draft-js/commit/6ba124cf663b78c41afd6c361a67bd29724fa617, to be released.
      // $FlowFixMe
      entityType.type,
      "MUTABLE",
      data,
    );
    const entityKey = contentStateWithEntity.getLastCreatedEntityKey();
    const nextState = RichUtils.toggleLink(
      editorState,
      editorState.getSelection(),
      entityKey,
    );

    onComplete(nextState);
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
        contentLabel="Link chooser"
      >
        <form className="non-admin-draftail__LinkSource" onSubmit={this.onConfirm}>
          <div className="non-admin-draftail__LinkSource__field">
            <label htmlFor="url">Link URL</label>
            <input
              ref={(inputRef) => {
                this.inputRef = inputRef;
              }}
              name="url"
              type="text"
              onChange={this.onChangeURL}
              onBlur={this.onBlurURL}
              value={url}
              placeholder="www.example.com"
            />
            {this.state.validationError && <p className="non-admin-draftail__LinkSource__validationError">
              {this.state.validationError}
            </p>}
          </div>
          <button disabled={this.state.validationError} type="submit">Save</button>
        </form>
      </Modal>
    );
  }
}

const isValidUrl = url => {
  const validUrlPattern = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/;
  return validUrlPattern.test(url.toLowerCase());
};

export default LinkSource;
