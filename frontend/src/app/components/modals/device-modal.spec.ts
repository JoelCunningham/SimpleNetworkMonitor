import { DeviceModal } from '#components/modals';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('DeviceModal', () => {
  let component: DeviceModal;
  let fixture: ComponentFixture<DeviceModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DeviceModal],
    }).compileComponents();

    fixture = TestBed.createComponent(DeviceModal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
