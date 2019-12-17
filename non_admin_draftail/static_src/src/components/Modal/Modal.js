import React from "react";
import ReactModal from "react-modal";
import "./Modal.scss";

const className = {
  base: "non_admin_draftail__modal",
  afterOpen: "non_admin_draftail__modal--open",
  beforeClose: "non_admin_draftail__modal--before-close",
};

const overlayClassName = {
  base: "non_admin_draftail__modal__overlay",
  afterOpen: "non_admin_draftail__modal__overlay--open",
  beforeClose: "non_admin_draftail__modal__overlay--before-close",
};

const Modal = (props) => (
  <ReactModal
    className={className}
    overlayClassName={overlayClassName}
    bodyOpenClassName="non_admin_draftail__modal__container--open"
    portalClassName="non_admin_draftail__portal"
    {...props}
  />
);

export default Modal;