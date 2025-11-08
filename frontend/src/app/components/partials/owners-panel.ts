import { BasePanel } from '#components/base/base-panel/base-panel';
import { BasicCard } from '#components/cards/basic-card';
import { OwnerForm } from '#components/forms/owner-form';
import { Modal } from '#components/partials/modal';
import { Owner } from '#interfaces/owner';
import { OwnerService } from '#services/owner-service';
import { FormMode } from '#types/form-mode';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-owners-panel',
  imports: [BasePanel, OwnerForm, Modal, BasicCard],
  templateUrl: './owners-panel.html',
  styleUrl: './owners-panel.scss',
})
export class OwnersPanel implements OnInit {
  owners: Owner[] = [];
  currentOwner: Owner | null = null;
  showOwnerModal = false;
  ownerFormMode: FormMode | null = null;

  constructor(
    private ownerService: OwnerService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.ownerService.currentOwners().subscribe((data) => {
      this.owners = data.sort((a, b) => {
        const deviceDiff = (b.devices.length || 0) - (a.devices.length || 0);
        if (deviceDiff !== 0) return deviceDiff;
        return (a.name || '').localeCompare(b.name || '');
      });
      this.cdr.detectChanges();
    });
  }

  openViewModal(owner: Owner) {
    this.currentOwner = owner;
    this.ownerFormMode = FormMode.View;
    this.showOwnerModal = true;
  }

  openAddModal() {
    this.currentOwner = { id: 0, name: '', devices: [] };
    this.ownerFormMode = FormMode.Add;
    this.showOwnerModal = true;
  }

  closeModal() {
    this.showOwnerModal = false;
    setTimeout(() => {
      this.ownerFormMode = null;
      this.currentOwner = null;
      this.cdr.detectChanges();
    }, 100);
  }

  getModalTitle(): string | null {
    switch (this.ownerFormMode) {
      case FormMode.Add:
        return 'Add Owner';
      case FormMode.View:
        return 'View Owner';
      case FormMode.Edit:
        return 'Edit Owner';
      default:
        return null;
    }
  }

  hasOwners(): boolean {
    return this.owners.length > 0;
  }

  handleOwnerUpdate(owner: Owner) {
    const ownerIndex = this.owners.findIndex((o) => o.id === owner.id);
    if (ownerIndex !== -1) {
      this.owners[ownerIndex] = owner;
    } else {
      this.owners.push(owner);
    }
  }

  handleOwnerDelete(owner: Owner) {
    this.owners = this.owners.filter((o) => o.id !== owner.id);
    this.currentOwner = null;
    this.showOwnerModal = false;
  }
}
